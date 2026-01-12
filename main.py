import hmac
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from dotenv import load_dotenv

from fastapi import BackgroundTasks, FastAPI, File, Header, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from rag import RagIndex, build_index_from_dir, get_storage_paths, load_index, save_index

# Load environment variables from .env file
load_dotenv()


def _env(name: str, default: Optional[str] = None) -> str:
    val = os.environ.get(name, default)
    if val is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return val


GITHUB_TOKEN = _env("GITHUB_TOKEN")
ADMIN_TOKEN = _env("ADMIN_TOKEN")

GITHUB_MODELS_ENDPOINT = os.environ.get("GITHUB_MODELS_ENDPOINT", "https://models.inference.ai.azure.com")
GITHUB_MODELS_CHAT_MODEL = os.environ.get("GITHUB_MODELS_CHAT_MODEL", "gpt-4o")

RAG_STORAGE_DIR = Path(os.environ.get("RAG_STORAGE_DIR", "./rag_storage")).resolve()

ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get("ALLOWED_ORIGINS", "").split(",")
    if o.strip()
]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    messages: List[ChatMessage] = Field(default_factory=list)


class Citation(BaseModel):
    source: str
    chunk_id: str
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)


app = FastAPI()

if ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,
    )


def _admin_guard(x_admin_token: Optional[str]) -> None:
    if not x_admin_token:
        raise HTTPException(status_code=401, detail="Missing X-Admin-Token")
    if not hmac.compare_digest(x_admin_token, ADMIN_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid admin token")


from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

def rate_limit_custom_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too Many Requests"}
    )

app.add_exception_handler(RateLimitExceeded, rate_limit_custom_handler)


client = ChatCompletionsClient(
    endpoint=GITHUB_MODELS_ENDPOINT,
    credential=AzureKeyCredential(GITHUB_TOKEN),
)


_rag_index: Optional[RagIndex] = None

try:
    # Optional: available in newer SDK versions.
    from azure.ai.inference.models import AssistantMessage  # type: ignore
except Exception:  # pragma: no cover
    AssistantMessage = None  # type: ignore


def _load_or_init_index() -> None:
    global _rag_index
    pdf_dir, storage_dir = get_storage_paths(RAG_STORAGE_DIR)
    idx = load_index(storage_dir)
    if idx is None:
        # If no index found but we have PDFs (e.g. first deploy from git), build it.
        if list(pdf_dir.glob("*.pdf")):
            print("No index found. Building from PDFs...")
            idx = build_index_from_dir(pdf_dir)
            save_index(idx, storage_dir)
    _rag_index = idx


@app.on_event("startup")
def _startup() -> None:
    _load_or_init_index()


@app.get("/api/health")
def health() -> Dict[str, Any]:
    pdf_dir, storage_dir = get_storage_paths(RAG_STORAGE_DIR)
    pdf_count = len(list(pdf_dir.glob("*.pdf")))
    has_index = (storage_dir / "chunks.json").exists() and (storage_dir / "tokens.json").exists()
    return {
        "ok": True,
        "model": GITHUB_MODELS_CHAT_MODEL,
        "pdfCount": pdf_count,
        "hasIndex": has_index,
    }


def _rebuild_index() -> None:
    global _rag_index
    pdf_dir, storage_dir = get_storage_paths(RAG_STORAGE_DIR)
    idx = build_index_from_dir(pdf_dir)
    save_index(idx, storage_dir)
    _rag_index = idx


@app.post("/api/admin/reindex")
def admin_reindex(
    background: BackgroundTasks,
    x_admin_token: Optional[str] = Header(default=None, alias="X-Admin-Token"),
) -> Dict[str, Any]:
    _admin_guard(x_admin_token)
    background.add_task(_rebuild_index)
    return {"ok": True, "status": "reindex_scheduled"}


@app.post("/api/admin/upload-pdf")
async def admin_upload_pdf(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    x_admin_token: Optional[str] = Header(default=None, alias="X-Admin-Token"),
) -> Dict[str, Any]:
    _admin_guard(x_admin_token)
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf uploads are supported")

    pdf_dir, _ = get_storage_paths(RAG_STORAGE_DIR)
    target = pdf_dir / file.filename

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    target.write_bytes(content)
    background.add_task(_rebuild_index)
    return {"ok": True, "savedAs": file.filename, "status": "reindex_scheduled"}


def _format_context(retrieved: List[Dict[str, Any]]) -> str:
    if not retrieved:
        return "No documents available."
    parts: List[str] = []
    for i, item in enumerate(retrieved, start=1):
        parts.append(
            f"[{i}] source={item['source']} chunk_id={item['chunk_id']}\n{item['text']}"
        )
    return "\n\n---\n\n".join(parts)


@app.post("/api/chat")
@limiter.limit("5/minute")
async def chat(req: ChatRequest, request: Request):
    # ip = request.client.host if request.client else "unknown" (Handled by slowapi)

    idx = _rag_index
    retrieved: List[Dict[str, Any]] = []
    if idx is not None:
        # Cross-lingual bridge: BM25 is keyword-based. If the query is Arabic but documents are English,
        # we append English keywords to help retrieval find the right chunks.
        search_query = req.question
        # Identify specific intent (Projects vs Experience)
        is_project_query = any(kw in search_query for kw in ["مشروع", "مشاريع", "اعمال", "أعمال", "project"])
        
        arabic_keywords = [
            "احمد", "أحمد", "محمد", "عبد السلام", "عبدالسلام",
            "مشروع", "مشاريع", "اعمال", "أعمال",
            "خبرة", "مهارات", "سيرة", "CV", "تعليم"
        ]
        
        if any(kw in search_query for kw in arabic_keywords):
            # If they ask for projects, we prioritize project keywords to avoid dilution
            if is_project_query:
                search_query += " Ahmed Mohamed Projects Featured"
            else:
                search_query += " Ahmed Mohamed Abdulsalam Experience Skills CV"
            
        # Increased top_k to 12 to ensure we don't miss chunks like "Project List" 
        # which might rank lower than "Bio/Header" chunks.
        hits = idx.retrieve(search_query, top_k=12)
        for chunk, _score in hits:
            retrieved.append(
                {
                    "source": chunk.source,
                    "chunk_id": chunk.id,
                    "text": chunk.text,
                }
            )

    system_prompt = (
        "You are the personal portfolio assistant for Ahmed Mohamed Ahmed Abdulsalam (احمد محمد احمد عبد السلام).\n"
        "The user may refer to him as Ahmed, Ahmed Mohamed, Ahmed Abdulsalam, or simply 'احمد'. All these refer to the portfolio owner.\n"
        "Explain his projects, skills, and experience using the provided DOCUMENT_CONTEXT (mostly in English).\n"
        "IMPORTANT: You MUST respond in the same language as the user's latest query. If they ask in Arabic, respond in Arabic using the English context as your source of truth.\n"
        "If the information is not in the context, politely state that your knowledge is limited to the provided documents.\n"
        "Be concise, professional, and helpful.\n"
        "\n"
        "DOCUMENT_CONTEXT:\n"
        f"{_format_context(retrieved)}"
    )

    # We keep previous turns from the browser to allow multi-turn chat,
    # but we DO NOT accept 'system' messages from the client.
    messages: List[Any] = [SystemMessage(system_prompt)]
    for m in req.messages[-12:]:
        if m.role == "user":
            messages.append(UserMessage(m.content))
        else:
            if AssistantMessage is not None:
                messages.append(AssistantMessage(m.content))
            else:
                # Fallback if SDK doesn't support AssistantMessage.
                messages.append(UserMessage(f"(assistant said) {m.content}"))

    messages.append(UserMessage(req.question))

    citations = [
        Citation(
            source=item["source"],
            chunk_id=item["chunk_id"],
            excerpt=item["text"][:220] + ("..." if len(item["text"]) > 220 else ""),
        )
        for item in retrieved[:4]
    ]

    async def event_generator():
        # 1. Send citations first
        yield f"data: {json.dumps({'type': 'citations', 'citations': [c.model_dump() for c in citations]}, ensure_ascii=False)}\n\n"

        try:
            # 2. Stream the response
            response = client.complete(
                messages=messages,
                model=GITHUB_MODELS_CHAT_MODEL,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield f"data: {json.dumps({'type': 'content', 'content': content}, ensure_ascii=False)}\n\n"
            
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'detail': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


