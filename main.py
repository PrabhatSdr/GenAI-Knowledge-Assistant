from fastapi import FastAPI

from api.upload import router as upload_router
from api.chat import router as chat_router
from api.history import router as history_router
from api.documents import router as document_router

app = FastAPI(
    title="GenAI Research & Knowledge Assistant",
    description="A full-stack Generative AI platform using RAG, Agents, Memory, and Local LLMs.",
    version="1.0.0"
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