import os
import shutil
import uuid

from fastapi import APIRouter, UploadFile, File

from config.settings import settings
from services.ingestion_service import IngestionService

router = APIRouter()

ingestion_service = IngestionService()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Accept only PDFs
    if not file.filename.endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed."
        }

    # Create upload directory if needed
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}.pdf"

    file_path = os.path.join(
        settings.UPLOAD_FOLDER,
        unique_filename
    )

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Automatically ingest the PDF
    result = ingestion_service.ingest(file_path)

    return {
        "message": "PDF uploaded and indexed successfully.",
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "ingestion": result
    }