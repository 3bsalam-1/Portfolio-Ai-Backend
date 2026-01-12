# 🤖 Portfolio AI Backend

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![GitHub Models](https://img.shields.io/badge/GitHub-Models-black?logo=github&logoColor=white)](https://docs.github.com/en/github-models)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](README.md)

> A production-ready FastAPI backend powering AI-driven portfolio chatbot with **Retrieval-Augmented Generation (RAG)** over PDFs using **GitHub Models**.

[Quick Start](#quick-start) • [API Docs](#api-documentation) • [Deploy](#deployment) • [Contributing](#development)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Deployment](#deployment)
- [Architecture](#architecture)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 📖 Overview

Portfolio AI Backend is a FastAPI service that powers an intelligent chatbot capable of answering questions about a portfolio based on PDF documents. It combines **GitHub Models** (gpt-4o by default) with a lightweight **Retrieval-Augmented Generation (RAG)** system using BM25 lexical search for document retrieval.

### 🎯 Key Capabilities

- **🤖 AI-Powered Chat**: Uses GitHub Models API for intelligent, context-aware responses
- **📚 RAG System**: Retrieves relevant document chunks from uploaded PDFs
- **💬 Multi-turn Conversations**: Maintains conversation history for context-aware responses
- **🔐 Admin Controls**: Secure endpoints for PDF management and index rebuilding
- **⏱️ Rate Limiting**: Built-in protection against abuse (5 requests/minute)
- **🔗 CORS Support**: Configurable cross-origin resource sharing for frontend integration
- **💚 Health Monitoring**: Endpoint for system status and index health checks

---

## ⚡ Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/portfolio-ai-backend.git
cd portfolio-ai-backend

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export GITHUB_TOKEN="your_token_here"
export ADMIN_TOKEN="your_admin_secret"

# 5. Run server
uvicorn main:app --reload --port 8000
```

**API is live at:** `http://localhost:8000`
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## ✨ Features

| Feature | Status | Details |
|---------|--------|---------|
| FastAPI with async support | ✅ | High concurrency, production-ready |
| GitHub Models integration | ✅ | Via Azure AI Inference SDK |
| Lightweight RAG (BM25) | ✅ | Document retrieval & chunking |
| PDF parsing | ✅ | Automatic text extraction & chunking |
| Token authentication | ✅ | HMAC-verified admin tokens |
| Rate limiting | ✅ | 5 requests/minute per IP |
| CORS middleware | ✅ | Configurable origins |
| Error handling | ✅ | Comprehensive exception handling |
| Docker support | ✅ | Production-ready container |

## 📋 Overview

Portfolio AI Backend is a FastAPI service that powers an intelligent chatbot capable of answering questions about a portfolio based on PDF documents. It combines GitHub Models (gpt-4o by default) with a lightweight Retrieval-Augmented Generation (RAG) system using BM25 lexical search for document retrieval.

### Key Capabilities

- **AI-Powered Chat**: Uses GitHub Models API for intelligent, context-aware responses
- **RAG System**: Retrieves relevant document chunks from uploaded PDFs
- **Multi-turn Conversations**: Maintains conversation history for context-aware responses
- **Admin Controls**: Secure endpoints for PDF management and index rebuilding
- **Rate Limiting**: Built-in protection against abuse (5 requests/minute)
- **CORS Support**: Configurable cross-origin resource sharing for frontend integration
- **Health Monitoring**: Endpoint for system status and index health checks

## Features

- ✅ FastAPI with async support for high concurrency
- ✅ GitHub Models integration via Azure AI Inference SDK
- ✅ Lightweight RAG with BM25-based document retrieval
- ✅ PDF parsing and automatic chunking with overlap
- ✅ Persistent storage with JSON-based index
- ✅ Token-based authentication for admin endpoints
- ✅ HMAC-verified admin tokens for security
- ✅ Rate limiting with slowapi
- ✅ CORS middleware for frontend integration
- ✅ Comprehensive error handling
- ✅ Container-ready (Dockerfile included)

## 📦 Prerequisites

- **Python 3.9+** – [Download](https://www.python.org/downloads/)
- **GitHub Account** – with access to [GitHub Models](https://docs.github.com/en/github-models)
- **GITHUB_TOKEN** – Personal access token from GitHub
- **ADMIN_TOKEN** – Custom secret for protecting admin endpoints

### 🔑 Get Your GitHub Token

1. Visit [GitHub Settings > Developer Settings > Personal access tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Grant `read:user` scope minimum
4. Copy and save the token securely ⚠️

---

## 🚀 Installation

## 🚀 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/portfolio-ai-backend.git
   cd portfolio-ai-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GITHUB_TOKEN=your_github_token_here
   ADMIN_TOKEN=your_secure_admin_token_here
   ```

5. **Run the development server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The API will be available at:
   - Main: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs` 🎨
   - ReDoc: `http://localhost:8000/redoc` 📖

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | ✅ | - | GitHub personal access token for Models API |
| `ADMIN_TOKEN` | ✅ | - | Secret token for protecting admin endpoints |
| `GITHUB_MODELS_ENDPOINT` | ❌ | `https://models.inference.ai.azure.com` | GitHub Models API endpoint |
| `GITHUB_MODELS_CHAT_MODEL` | ❌ | `gpt-4o` | Default LLM model to use |
| `RAG_STORAGE_DIR` | ❌ | `./rag_storage` | Directory for PDFs and index storage |
| `ALLOWED_ORIGINS` | ❌ | - | Comma-separated CORS origins (e.g., `https://example.com,https://app.example.com`) |

### Storage Structure

```
RAG_STORAGE_DIR/
├── pdfs/                    # Uploaded PDF files
│   ├── resume.pdf
│   ├── projects.pdf
│   └── ...
├── chunks.json             # Serialized document chunks
└── tokens.json             # Tokenized corpus for BM25
```

## 🔌 API Documentation

### 1️⃣ Health Check

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "ok": true,
  "model": "gpt-4o",
  "pdfCount": 3,
  "hasIndex": true
}
```

**Use Case:** Monitor service availability and RAG index status

---

### 2️⃣ Chat (Main Endpoint)

**Endpoint:** `POST /api/chat`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "What are Ahmed's main projects?",
  "messages": [
    {
      "role": "user",
      "content": "Tell me about your background"
    },
    {
      "role": "assistant",
      "content": "I'm a software engineer with 5 years of experience..."
    }
  ]
}
```

**Response:**
```json
{
  "answer": "Ahmed has worked on several projects including...",
  "citations": [
    {
      "source": "resume.pdf",
      "chunk_id": "resume.pdf:3",
      "excerpt": "Project 1: ML Pipeline..."
    }
  ]
}
```

**Rate Limit:** 5 requests per minute per IP ⏱️

**Notes:**
- `messages` array supports up to 12 previous turns for context
- Only `user` and `assistant` roles are supported
- System messages from clients are ignored for security 🔒
- Citations limited to top 4 retrieved chunks

---

### 3️⃣ Upload PDF (Admin)

**Endpoint:** `POST /api/admin/upload-pdf`

**Headers:**
```
X-Admin-Token: your_admin_token_here
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: PDF file (binary)

**Response:**
```json
{
  "ok": true,
  "savedAs": "resume.pdf",
  "status": "reindex_scheduled"
}
```

**Notes:**
- Only `.pdf` files are accepted
- Reindexing happens asynchronously in the background 🔄
- Maximum file size depends on Uvicorn configuration

---

### 4️⃣ Rebuild Index (Admin)

**Endpoint:** `POST /api/admin/reindex`

**Headers:**
```
X-Admin-Token: your_admin_token_here
```

**Response:**
```json
{
  "ok": true,
  "status": "reindex_scheduled"
}
```

**Notes:**
- Reindexes all PDFs in `pdfs/` directory
- Process runs asynchronously in background 🔄
- Useful after adding/removing PDFs directly

---

### ❌ Error Responses

| Status | Error | Cause |
|--------|-------|-------|
| 400 | Invalid request | Malformed JSON, invalid file type, empty file |
| 401 | Missing X-Admin-Token | Admin token not provided in header |
| 403 | Invalid admin token | Admin token is incorrect or expired |
| 429 | Too Many Requests | Rate limit exceeded ⏱️ |
| 502 | Upstream model error | GitHub Models API error |

---

## 📚 API Documentation

## 💻 Usage Examples

### Example 1: Single-Turn Chat

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is my experience with machine learning?",
    "messages": []
  }'
```

### Example 2: Multi-Turn Conversation

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Can you elaborate on that?",
    "messages": [
      {
        "role": "user",
        "content": "What is my experience with machine learning?"
      },
      {
        "role": "assistant",
        "content": "Based on your resume, you have 3 years of ML experience..."
      }
    ]
  }'
```

### Example 3: Upload PDF

```bash
curl -X POST "http://localhost:8000/api/admin/upload-pdf" \
  -H "X-Admin-Token: your_secure_admin_token" \
  -F "file=@./resume.pdf"
```

### Example 4: Trigger Reindex

```bash
curl -X POST "http://localhost:8000/api/admin/reindex" \
  -H "X-Admin-Token: your_secure_admin_token"
```

### Example 5: Check Health

```bash
curl -X GET "http://localhost:8000/api/health"
```

---

## 🌐 Deployment

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t portfolio-ai-backend:latest .
   ```

2. **Run locally**
   ```bash
   docker run -p 8000:8000 \
     -e GITHUB_TOKEN="your_token" \
     -e ADMIN_TOKEN="your_token" \
     -e ALLOWED_ORIGINS="https://yourdomain.com" \
     -v rag_storage:/app/rag_storage \
     portfolio-ai-backend:latest
   ```

### 🚀 Render.com Deployment

1. **Connect your GitHub repository**
2. **Create a new Web Service**
3. **Set environment variables in Dashboard**:
   - `GITHUB_TOKEN` 🔑
   - `ADMIN_TOKEN` 🔑
   - `ALLOWED_ORIGINS`
4. **Attach a persistent disk** for `RAG_STORAGE_DIR`:
   ```
   RAG_STORAGE_DIR=/var/data
   ```
5. **Deploy** - the service will start automatically ✅

### 🛠️ Environment-Specific Configuration

**Development:**
```bash
GITHUB_MODELS_CHAT_MODEL=gpt-4o
RAG_STORAGE_DIR=./rag_storage
```

**Production:**
```bash
GITHUB_MODELS_CHAT_MODEL=gpt-4o
RAG_STORAGE_DIR=/var/data
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Client                          │
│            (React, Vue, or any web framework)               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Server                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  /api/chat               (Rate Limited: 5/min)       │  │
│  │  /api/health                                          │  │
│  │  /api/admin/upload-pdf   (Token Protected)           │  │
│  │  /api/admin/reindex      (Token Protected)           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    ┌─────────┐ ┌─────────┐ ┌──────────┐
    │  RAG    │ │ Azure AI│ │ Env      │
    │ Module  │ │ Inference
    │ (BM25)  │ │ (LLM)   │ │ Config   │
    └────┬────┘ └─────────┘ └──────────┘
         │
         ▼
    ┌──────────────────┐
    │ Persistent Disk  │
    │  /rag_storage/   │
    │  ├── pdfs/       │
    │  ├── chunks.json │
    │  └── tokens.json │
    └──────────────────┘
```

### 🔄 RAG Pipeline

1. **📤 PDF Upload**: Admin uploads PDF via `/api/admin/upload-pdf`
2. **📄 Text Extraction**: PDF → plaintext using `pypdf`
3. **✂️ Chunking**: Text split into 1100-char chunks with 180-char overlap
4. **🔤 Tokenization**: Chunks tokenized using regex [A-Za-z0-9_]+
5. **🔍 Indexing**: BM25 corpus built and serialized to JSON
6. **🎯 Retrieval**: Query → BM25 scores → Top-k chunks
7. **📋 Context Building**: Chunks formatted into system prompt
8. **🤖 LLM Query**: System prompt + history + query → GitHub Models API
9. **💬 Response**: Answer + citations returned to client

### 📂 Key Files

| File | Lines | Purpose |
|------|-------|---------|
| `main.py` | 263 | FastAPI app, endpoints, request handling |
| `rag.py` | 152 | RAG logic, PDF parsing, BM25 retrieval |
| `requirements.txt` | - | Python dependencies |
| `Dockerfile` | - | Container configuration |

---

## 👨‍💻 Development

### 📦 Project Structure

```
portfolio-ai-backend/
├── main.py                 # FastAPI app & endpoints
├── rag.py                  # RAG implementation
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── LICENSE                 # MIT License
├── render.yaml             # Render deployment config
├── README.md               # This file
└── rag_storage/            # Persistent storage (gitignored)
    ├── pdfs/               # Uploaded PDFs
    ├── chunks.json         # Document chunks
    └── tokens.json         # Tokenized corpus
```

### 🧪 Running Tests

Currently, there is no automated test suite. Validate endpoints manually:

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"test","messages":[]}'

# View interactive docs
open http://localhost:8000/docs
```

### 📋 Code Conventions

- **Environment Variables**: Use `_env(name, default)` helper in main.py
- **Error Handling**: FastAPI `HTTPException` for API errors
- **Admin Guards**: `_admin_guard()` validates X-Admin-Token header
- **Rate Limiting**: slowapi decorator on public endpoints
- **RAG Indexing**: Async background tasks via `BackgroundTasks`

---

## 🐛 Troubleshooting

### ⚠️ Common Issues

**Issue: "Missing required env var: GITHUB_TOKEN"**
- ✅ Solution: Ensure `GITHUB_TOKEN` is set in `.env` or environment

**Issue: "Invalid admin token"**
- ✅ Solution: Verify `X-Admin-Token` header matches `ADMIN_TOKEN` env var

**Issue: "RAG index is empty after upload"**
- ✅ Solution: Check that PDF upload completed successfully and reindex was triggered

**Issue: "Rate limit exceeded (429)"**
- ✅ Solution: Space chat requests to at least 12 seconds apart (5/min limit)

**Issue: "Upstream model error"**
- ✅ Solution: Verify GitHub token is valid and has access to GitHub Models API

### 🔧 Debug Mode

Enable FastAPI debug mode:

```python
app = FastAPI(debug=True)  # in main.py
```

View auto-generated API documentation:
- 🎨 **Swagger UI**: `http://localhost:8000/docs`
- 📖 **ReDoc**: `http://localhost:8000/redoc`

### 📊 Logging

The application outputs logs to stdout. For production, integrate with:
- Render's log aggregation
- CloudWatch (if using AWS)
- Datadog, Sentry, or similar observability platforms

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive open-source license that allows:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Requires attribution (copyright notice)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📞 Support

**Need Help?**
- 📖 Check the [GitHub Issues](https://github.com/yourusername/portfolio-ai-backend/issues)
- 📚 Review [GitHub Models Documentation](https://docs.github.com/en/github-models)
- 💬 Create a [Discussion](https://github.com/yourusername/portfolio-ai-backend/discussions)
- 📧 Contact: [Email](mailto:3bsalam0@gmail.com)

---

<div align="center">

**Made with ❤️ by Ahmed Abdulsalam**

Give us a ⭐ if you found this project helpful!

</div>
