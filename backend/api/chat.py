from fastapi import APIRouter
from pydantic import BaseModel

from rag.rag_pipeline import RAGPipeline

router = APIRouter()

pipeline = RAGPipeline()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest, chat_id: str = "default"):

    response = pipeline.ask(
        question=request.question,
        chat_id=chat_id
    )

    return response