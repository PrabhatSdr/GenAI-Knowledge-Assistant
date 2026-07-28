from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.upload import router as upload_router
from api.chat import router as chat_router
from api.history import router as history_router
from api.documents import router as document_router

app = FastAPI(
    title="GenAI Research & Knowledge Assistant",
    description="A full-stack Generative AI platform using RAG, Agents, Memory, and Local LLMs.",
    version="1.0.0"
)

# Allow the Next.js dev server (localhost:3000) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    upload_router,
    prefix="/api",
    tags=["Upload"]
)

app.include_router(
    chat_router,
    prefix="/api",
    tags=["Chat"]
)

app.include_router(
    history_router,
    prefix="/api",
    tags=["History"]
)

app.include_router(
    document_router,
    prefix="/api",
    tags=["Documents"]
)


@app.get("/")
def home():
    return {
        "message": "GenAI Research & Knowledge Assistant API is running."
        }