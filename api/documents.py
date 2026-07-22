from fastapi import APIRouter, HTTPException

from services.document_service import DocumentService

router = APIRouter()

document_service = DocumentService()


@router.get("/documents")
def list_documents():

    return {
        "count": document_service.get_document_count(),
        "documents": document_service.list_documents(),
    }


@router.get("/documents/count")
def count_documents():

    return {
        "count": document_service.get_document_count()
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