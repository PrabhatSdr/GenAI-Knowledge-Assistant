from fastapi import APIRouter, HTTPException

from services.document_service import DocumentService

router = APIRouter()

document_service = DocumentService()


@router.get("/documents")
def list_documents(chat_id: str = "default"):

    docs = document_service.list_documents(chat_id=chat_id)

    return {
        "count": len(docs),
        "documents": docs,
    }


@router.get("/documents/count")
def count_documents(chat_id: str = "default"):

    return {
        "count": document_service.get_document_count(chat_id=chat_id)
    }


@router.get("/documents/{filename}")
def get_document(filename: str):

    document = document_service.get_document(filename)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return document


@router.delete("/documents/{filename}")
def delete_document(filename: str):

    success = document_service.delete_document(filename)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "message": f"{filename} deleted successfully."
    }