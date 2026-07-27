# GenAI Knowledge Assistant

A full-stack, **fully local** Retrieval-Augmented Generation (RAG) chat app.
Upload PDFs, ask questions about them, and keep multiple conversations —
each chat scopes to its own documents.

```
┌────────────────┐      /api/*      ┌────────────────────┐
│  Next.js 16    │ ───────────────▶ │  FastAPI + Ollama  │
│  React 19 UI   │                  │  Qdrant (local)    │
│  Tailwind v4   │                  │  sentence-transformers │
└────────────────┘                  └────────────────────┘
   localhost:3000                      localhost:8000
```

| Folder | Stack | README |
|---|---|---|
| `frontend/` | Next.js 16 (App Router), React 19, TypeScript, Tailwind v4 | [`frontend/README.md`](./frontend/README.md) |
| `backend/`  | FastAPI, Ollama, Qdrant (embedded), sentence-transformers, LangChain text splitters | [`backend/README.md`](./backend/README.md) |

## Features

- 📄 **PDF upload** with automatic chunking, embedding, and indexing into Qdrant
- 💬 **Multi-turn chat** over your documents with retrieved context injected into every prompt
- 🗂️ **Per-chat document scope** — each chat only sees its own uploads (Qdrant filter on `chat_id`)
- 📚 **Persistent history** — every conversation is saved to `backend/memory/<chat_id>.json`
- 🗑️ **Delete chat / delete document** — cascades through Qdrant, metadata, and uploads folder
- 🔒 **Local-only** — LLM runs via Ollama, embeddings via `sentence-transformers`, vector store via embedded Qdrant. No external API calls.

## Quick start

You'll need **three** things running:
1. **Ollama** with at least one model pulled (`ollama pull llama3.2:3b`)
2. **Python venv** in `backend/` with deps installed
3. **Node deps** in `frontend/`

### 1. Install

```powershell
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ..\frontend
npm install
```

### 2. Configure

Copy/edit the env files:

- `backend/.env` — `OLLAMA_MODEL`, `EMBEDDING_MODEL`, `UPLOAD_FOLDER`, `QDRANT_PATH` (already populated with sensible defaults)
- `frontend/.env.local` — `NEXT_PUBLIC_API_URL=http://localhost:8000` (already set)

### 3. Run

You need **two terminals**:

**Terminal 1 — backend**
```powershell
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 — frontend**
```powershell
cd frontend
npm run dev
```

Open http://localhost:3000.

## How it works

```
User question
    │
    ▼
GET /api/history/{chat_id}     ← prior turns (load-time only)
    │
    ▼
POST /api/chat?chat_id=...     ← RAG pipeline
    │
    ├─▶ memory.get_history(chat_id)                ← conversation turns
    ├─▶ retriever.retrieve(question, chat_id)      ← Qdrant filter by chat_id
    │       └─▶ vector_store.search(...)           ← top-k cosine chunks
    ├─▶ LLMService.generate(prompt)                ← Ollama chat
    └─▶ memory.add(chat_id, "user"|"assistant", …) ← persist
```

Uploads flow similarly:

```
POST /api/upload?chat_id=...
    │
    ▼
IngestionService.ingest(file_path, chat_id)
    ├─▶ load → clean → chunk → embed
    ├─▶ vector_store.add_documents(..., chat_id)   ← Qdrant payload tag
    └─▶ metadata.add_document(..., chat_id)        ← metadata/documents.json
```

## Project layout

```
genai-knowledge-assistant/
├── backend/
│   ├── api/                    # FastAPI routers
│   │   ├── upload.py
│   │   ├── chat.py
│   │   ├── history.py
│   │   └── documents.py
│   ├── services/
│   │   ├── ingestion_service.py
│   │   ├── retrieval_service.py
│   │   ├── metadata_service.py
│   │   └── document_service.py
│   ├── rag/
│   │   ├── rag_pipeline.py
│   │   ├── vector_store.py
│   │   ├── chunker.py
│   │   ├── document_loader.py
│   │   └── text_cleaner.py
│   ├── core/
│   │   ├── llm.py              # Ollama wrapper
│   │   ├── memory.py           # file-based chat history
│   │   ├── prompts.py
│   │   └── database.py         # VectorStore singleton
│   ├── config/settings.py
│   ├── memory/                 # one <chat_id>.json per conversation
│   ├── metadata/documents.json # registered documents
│   ├── uploads/                # raw uploaded PDFs
│   └── vector_db/              # embedded Qdrant storage
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx            # 3-pane shell
│   │   └── globals.css
│   ├── components/
│   │   ├── HistorySidebar.tsx
│   │   ├── DocumentPanel.tsx
│   │   └── ChatPanel.tsx
│   └── lib/api.ts              # typed fetch wrappers
└── README.md                   # you are here
```

## API surface

All endpoints under `/api/`:

| Method | Path | Notes |
|---|---|---|
| `POST` | `/upload?chat_id=…` | multipart `file` field; ingests into the active chat |
| `POST` | `/chat?chat_id=…` | body `{question}`; returns `{answer, sources[]}` |
| `GET`  | `/history` | list all chats (one entry per saved file) |
| `POST` | `/history` | create an empty chat; body `{chat_id}` |
| `GET`  | `/history/{chat_id}` | load saved messages for a chat |
| `DELETE` | `/history/{chat_id}` | delete a chat |
| `GET`  | `/documents?chat_id=…` | list docs (filtered to the active chat by default) |
| `GET`  | `/documents/count?chat_id=…` | doc count |
| `GET`  | `/documents/{filename}` | one doc |
| `DELETE` | `/documents/{filename}` | delete doc + its Qdrant vectors |

## Default chat

The app boots with an active chat id of `default`. New chats are generated as
`chat-<timestamp>` when you click **+ New** in the sidebar. Documents uploaded
before per-chat scoping was introduced are automatically owned by `default`.

## Testing

A handful of one-shot scripts live in `backend/`:

```powershell
cd backend
.\venv\Scripts\activate
python test_emb.py        # embedding model smoke test
python test_collection.py # Qdrant collection smoke test
python test_memory.py     # memory store smoke test
python test_pipeline.py   # RAG pipeline smoke test
python test_retrieval.py  # retrieval smoke test
```

## License

Personal project — no license specified.
