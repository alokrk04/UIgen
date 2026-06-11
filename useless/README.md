# 🧠 Smart AI Document Insights

A production-ready, full-stack AI document intelligence platform that runs entirely on local AI models. Upload documents, get automatic executive insights, and chat with your documents — all powered by Ollama.

![Architecture](https://img.shields.io/badge/Frontend-Next.js_15-blue) ![Backend](https://img.shields.io/badge/Backend-FastAPI-green) ![AI](https://img.shields.io/badge/AI-Ollama_Local-purple)

## ✨ Features

- **📄 Multi-format Support**: PDF, DOCX, CSV, JSON, TXT
- **🧠 Automatic AI Insights**: Executive summaries, key findings, action items, risks
- **💬 Interactive Chat**: Multi-turn Q&A with source citations and streaming responses
- **🔍 Hybrid Retrieval**: Semantic + BM25 keyword search with score fusion
- **🔒 Privacy First**: Everything runs locally through Ollama — no cloud APIs
- **🌙 Dark/Light Mode**: Clean, modern enterprise UI
- **⚡ Real-time Status**: Live processing status updates with polling

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, TypeScript, Tailwind CSS, Zustand, React Query |
| Backend | FastAPI, Pydantic, Uvicorn, async architecture |
| AI | LangChain, Ollama (llama3/mistral + nomic-embed-text) |
| Vector DB | ChromaDB with persistent storage |

## 📋 Prerequisites

1. **Python 3.11+**
2. **Node.js 20+**
3. **Ollama** running locally with models installed:
   ```bash
   # Install Ollama (https://ollama.ai)
   ollama pull llama3
   ollama pull nomic-embed-text
   ```

## 🚀 Quick Start

### Option 1: Run Locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Server starts at `http://localhost:8000`

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
App opens at `http://localhost:3000`

### Option 2: Docker Compose

```bash
# Make sure Ollama is running locally
docker compose up --build
```

## 📁 Project Structure

```
smart-ai-doc-insights/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py             # Configuration settings
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile
│   ├── api/
│   │   └── routes.py         # API endpoints
│   ├── services/
│   │   ├── document_service.py   # Document processing orchestration
│   │   ├── chat_service.py       # RAG chat service
│   │   └── insights_service.py   # AI insights generation
│   ├── parsers/
│   │   ├── __init__.py       # Parser registry
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   ├── csv_parser.py
│   │   ├── json_parser.py
│   │   └── txt_parser.py
│   ├── rag/
│   │   ├── chunker.py        # Recursive text chunking
│   │   └── retriever.py      # Hybrid semantic + BM25 retrieval
│   ├── embeddings/
│   │   └── ollama_embeddings.py
│   ├── vectorstore/
│   │   └── chroma_store.py
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   └── utils/
│       └── file_utils.py
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx          # Main dashboard
│   │   └── globals.css
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── DocumentList.tsx
│   │   ├── UploadZone.tsx
│   │   ├── InsightsPanel.tsx
│   │   └── ChatPanel.tsx
│   ├── store/
│   │   └── app-store.ts      # Zustand state management
│   ├── lib/
│   │   └── api.ts            # API client
│   ├── types/
│   │   └── index.ts          # TypeScript types
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload a document |
| `POST` | `/api/process/{id}` | Reprocess a document |
| `GET` | `/api/documents` | List all documents |
| `GET` | `/api/documents/{id}` | Get document metadata |
| `DELETE` | `/api/documents/{id}` | Delete a document |
| `POST` | `/api/insights/{id}` | Generate AI insights |
| `POST` | `/api/chat` | Chat with a document |
| `POST` | `/api/chat/stream` | Stream chat responses (SSE) |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/ollama/status` | Ollama connectivity status |

## 🔄 Processing Pipeline

1. **Upload** → File validation (type, size, corruption check)
2. **Parse** → Format-specific text extraction with metadata
3. **Chunk** → RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
4. **Embed** → Local embeddings via Ollama (nomic-embed-text)
5. **Store** → ChromaDB with per-document collections
6. **Retrieve** → Hybrid search (semantic + BM25 keyword)

## ⚙️ Configuration

Environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `CHAT_MODEL` | `llama3` | LLM model for chat/insights |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Embedding model |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed CORS origins |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000/api` | Backend API URL |

## 📜 License

MIT
