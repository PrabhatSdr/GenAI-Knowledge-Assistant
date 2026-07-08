from fastapi import APIRouter
from pydantic import BaseModel
from rag.rag_pipeline import RAGPipeline

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    pipeline = RAGPipeline()

    return pipeline.ask(request.question)