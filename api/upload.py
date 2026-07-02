import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from rag.document_loader import extract_text_from_pdf

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    extracted_text = extract_text_from_pdf(file_path)

    return {
        "message": "PDF uploaded and text extracted successfully.",
        "file_id": file_id,
        "filename": file.filename,
        "file_path": file_path,
        "text_preview": extracted_text[:1000],
        "total_characters": len(extracted_text)
    }