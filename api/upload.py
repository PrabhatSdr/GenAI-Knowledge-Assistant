import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from rag.document_loader import extract_text_from_pdf
from rag.text_cleaner import clean_text
from rag.chunker import split_into_chunks

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        file_id = str(uuid.uuid4())
        safe_filename = file.filename.replace(" ", "_")
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{safe_filename}")

        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        extracted_text = extract_text_from_pdf(file_path)
        cleaned_text = clean_text(extracted_text)
        chunks = split_into_chunks(cleaned_text)

        return {
            "message": "PDF uploaded, cleaned, and chunked successfully.",
            "file_id": file_id,
            "filename": file.filename,
            "characters": len(cleaned_text),
            "chunks": len(chunks),
            "preview": chunks[0].page_content if chunks else "No readable text found in this PDF."
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )