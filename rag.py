import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import pdfplumber
from rank_bm25 import BM25Okapi


def _normalize_text(text: str) -> str:
    text = text.replace("\u0000", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


_token_re = re.compile(r"[A-Za-z0-9_]+")


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _token_re.findall(text)]


@dataclass(frozen=True)
class RagChunk:
    id: str
    source: str  # filename
    text: str


class RagIndex:
    def __init__(self, chunks: List[RagChunk], tokenized: List[List[str]]):
        self.chunks = chunks
        self._bm25 = BM25Okapi(tokenized)

    def retrieve(self, query: str, top_k: int = 6) -> List[Tuple[RagChunk, float]]:
        if not self.chunks:
            return []
        q = _tokenize(query)
        if not q:
            return []
        scores = self._bm25.get_scores(q)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        out: List[Tuple[RagChunk, float]] = []
        for idx, score in ranked:
            if score <= 0:
                continue
            out.append((self.chunks[idx], float(score)))
        return out


def load_pdf_text(pdf_path: Path) -> str:
    parts: List[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            txt = _normalize_text(txt)
            if txt:
                parts.append(txt)
    return "\n".join(parts).strip()


def chunk_text(
    text: str,
    *,
    chunk_size: int = 1100,
    overlap: int = 180,
) -> List[str]:
    if not text:
        return []
    if chunk_size <= 0:
        return []
    if overlap < 0:
        overlap = 0
    if overlap >= chunk_size:
        overlap = max(0, chunk_size // 4)

    chunks: List[str] = []
    i = 0
    n = len(text)
    while i < n:
        end = min(n, i + chunk_size)
        chunk = text[i:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        i = max(0, end - overlap)
    return chunks


def build_index_from_dir(
    pdf_dir: Path,
    *,
    chunk_size: int = 1100,
    overlap: int = 180,
) -> RagIndex:
    pdf_paths = sorted([p for p in pdf_dir.glob("*.pdf") if p.is_file()])
    chunks: List[RagChunk] = []
    tokenized: List[List[str]] = []

    for pdf_path in pdf_paths:
        text = load_pdf_text(pdf_path)
        for j, chunk in enumerate(chunk_text(text, chunk_size=chunk_size, overlap=overlap)):
            cid = f"{pdf_path.name}:{j}"
            rc = RagChunk(id=cid, source=pdf_path.name, text=chunk)
            chunks.append(rc)
            tokenized.append(_tokenize(chunk))

    return RagIndex(chunks, tokenized)


def _index_paths(storage_dir: Path) -> Tuple[Path, Path]:
    return storage_dir / "chunks.json", storage_dir / "tokens.json"


def save_index(index: RagIndex, storage_dir: Path) -> None:
    storage_dir.mkdir(parents=True, exist_ok=True)
    chunks_path, tokens_path = _index_paths(storage_dir)
    chunks_payload = [
        {"id": c.id, "source": c.source, "text": c.text} for c in index.chunks
    ]
    with chunks_path.open("w", encoding="utf-8") as f:
        json.dump(chunks_payload, f, ensure_ascii=False)

    # Rebuild tokenized corpus from stored text for portability
    tokenized = [_tokenize(c["text"]) for c in chunks_payload]
    with tokens_path.open("w", encoding="utf-8") as f:
        json.dump(tokenized, f, ensure_ascii=False)


def load_index(storage_dir: Path) -> Optional[RagIndex]:
    chunks_path, tokens_path = _index_paths(storage_dir)
    if not chunks_path.exists() or not tokens_path.exists():
        return None

    with chunks_path.open("r", encoding="utf-8") as f:
        chunks_payload = json.load(f)
    with tokens_path.open("r", encoding="utf-8") as f:
        tokenized = json.load(f)

    chunks = [RagChunk(**c) for c in chunks_payload]
    return RagIndex(chunks, tokenized)


def get_storage_paths(storage_dir: Path) -> Tuple[Path, Path]:
    pdf_dir = storage_dir / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    return pdf_dir, storage_dir

