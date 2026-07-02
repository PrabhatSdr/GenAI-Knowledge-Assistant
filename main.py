from fastapi import FastAPI
from pydantic import BaseModel
from core.llm import ask_llm
from api.upload import router as upload_router

app = FastAPI(
    title="GenAI Research & Knowledge Assistant",
    description="A full-stack Generative AI platform using RAG, Agents, Memory, and Local LLMs.",
    version="1.0.0"
)

app.include_router(upload_router, prefix="/api", tags=["Upload"])


class ChatRequest(BaseModel):
    message: str
    model: str = "llama3.2:3b"


@app.get("/")
def home():
    return {
        "message": "GenAI Research & Knowledge Assistant API is running."
    }


@app.post("/chat")
def chat(request: ChatRequest):
    response = ask_llm(
        prompt=request.message,
        model=request.model
    )

    return {
        "user_message": request.message,
        "model": request.model,
        "ai_response": response
    }