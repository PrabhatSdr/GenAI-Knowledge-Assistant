from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.memory import memory

router = APIRouter()


# -----------------------------
# List all chats
# -----------------------------
@router.get("/history")
def get_all_chats():

    return memory.list_chats()


# -----------------------------
# Create a new (empty) chat
# -----------------------------
class NewChatRequest(BaseModel):
    chat_id: str


@router.post("/history")
def create_chat(request: NewChatRequest):

    chat_id = request.chat_id.strip()

    if not chat_id:
        raise HTTPException(
            status_code=400,
            detail="chat_id cannot be empty."
        )

    # If it already exists, treat as success (idempotent)
    existing = memory.get_history(chat_id)

    return {
        "chat_id": chat_id,
        "messages": len(existing),
    }


# -----------------------------
# Load one chat
# -----------------------------
@router.get("/history/{chat_id}")
def get_chat(chat_id: str):

    return memory.load_chat(chat_id)


# -----------------------------
# Delete one chat
# -----------------------------
@router.delete("/history/{chat_id}")
def delete_chat(chat_id: str):

    deleted = memory.delete_chat(chat_id)

    if deleted:
        return {
            "message": "Conversation deleted successfully."
        }

    return {
        "message": "Conversation not found."
    }