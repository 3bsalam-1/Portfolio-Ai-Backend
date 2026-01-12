# Copilot Instructions for portfolio-ai-backend

## Project Overview

- This is a FastAPI backend for an AI chat system, integrating GitHub Models via `azure.ai.inference` and a lightweight RAG (Retrieval-Augmented Generation) over PDFs stored in `rag_storage/`.
- Key endpoints:
  - `GET /api/health`: Health check.
  - `POST /api/chat`: Main chat interface.
  - `POST /api/admin/upload-pdf`: Upload PDFs for RAG (admin only).
  - `POST /api/admin/reindex`: Rebuild RAG index (admin only).

## Architecture & Data Flow

- **Chat requests** are processed using GitHub Models (default: `gpt-4o`) via the Azure AI Inference SDK.
- **RAG**: PDFs are stored in `rag_storage/pdfs/`. Index and token data are in `rag_storage/chunks.json` and `rag_storage/tokens.json`.
- **Admin endpoints** require `ADMIN_TOKEN` for access.
- **Environment variables** control model endpoints, tokens, storage paths, and CORS origins. See README for details.

## Developer Workflows

- **Local development**:
  - Create a virtual environment and install dependencies from `requirements.txt`.
  - Set `GITHUB_TOKEN` and `ADMIN_TOKEN` in your environment.
  - Run with: `uvicorn main:app --reload --port 8000`
- **PDF Upload & Indexing**:
  - Use admin endpoints to upload PDFs and trigger reindexing.
  - Uploaded PDFs are stored in `rag_storage/pdfs/`.
- **Testing**: No explicit test suite; validate endpoints with tools like curl or Postman.

## Patterns & Conventions

- **RAG implementation** is in `rag.py` (see `RagIndex`, `RagChunk`, and BM25 retrieval logic).
- **Environment variable loading** uses `dotenv` and custom `_env()` helper in `main.py`.
- **Error handling**: Uses FastAPI's `HTTPException` for API errors.
- **CORS**: Origins are set via `ALLOWED_ORIGINS` env variable.
- **PDF parsing**: Uses `pypdf` for text extraction.

## Integration Points

- **GitHub Models**: Accessed via `azure.ai.inference` (see `main.py`).
- **RAG**: All PDF and index operations are in `rag.py` and `rag_storage/`.

## Examples

- To add a new endpoint, follow FastAPI patterns in `main.py`.
- To extend RAG, modify `RagIndex` in `rag.py` and update index logic.

## Key Files & Directories

- `main.py`: FastAPI app, endpoints, environment setup.
- `rag.py`: RAG logic, PDF parsing, BM25 retrieval.
- `rag_storage/`: Persistent storage for PDFs and index files.
- `requirements.txt`: Python dependencies.
- `README.md`: Setup and usage instructions.

---

For questions or unclear conventions, review `README.md` or ask for clarification.
