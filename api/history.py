from fastapi import APIRouter
from core.memory import memory

router = APIRouter()


# -----------------------------
# List all chats
# -----------------------------
@router.get("/history")
def get_all_chats():

    return memory.list_chats()


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