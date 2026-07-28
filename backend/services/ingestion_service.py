import os

from rag.document_loader import DocumentLoader
from rag.text_cleaner import TextCleaner
from rag.chunker import TextChunker

from services.embedding_service import EmbeddingService
from services.metadata_service import MetadataService
from core.database import vector_store


class IngestionService:

    def __init__(self):
        # Initialize helper classes
        self.loader = DocumentLoader()
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()
        self.embedder = EmbeddingService()
        self.metadata = MetadataService()

        # Ensure Qdrant collection exists
        vector_store.create_collection()

    def ingest(self, file_path: str, chat_id: str = "default"):

        print("=" * 60)
        print("Starting document ingestion...")
        print("=" * 60)

        # -----------------------------------
        # Step 1: Load PDF
        # -----------------------------------
        text = self.loader.load_pdf(file_path)
        print(f"Characters extracted: {len(text)}")

        # -----------------------------------
        # Step 2: Clean Text
        # -----------------------------------
        cleaned_text = self.cleaner.clean(text)
        print(f"Characters after cleaning: {len(cleaned_text)}")

        # -----------------------------------
        # Step 3: Chunk Text
        # -----------------------------------
        chunks = self.chunker.chunk_text(cleaned_text)
        print(f"Chunks created: {len(chunks)}")

        # -----------------------------------
        # Step 4: Generate Embeddings
        # -----------------------------------
        embeddings = self.embedder.embed_documents(chunks)
        print(f"Embeddings generated: {len(embeddings)}")

        # -----------------------------------
        # Step 5: Store in Qdrant
        # -----------------------------------
        filename = os.path.basename(file_path)

        vector_store.add_documents(
            chunks=chunks,
            embeddings=embeddings,
            filename=filename,
            chat_id=chat_id,
        )

        print("Document stored successfully!")
        print("=" * 60)

        # -----------------------------------
        # Step 6: Record Metadata
        # -----------------------------------
        # TODO: forward `original_filename` once api/upload.py is updated
        # to pass it through (currently the upload route doesn't share it).
        size_bytes = os.path.getsize(file_path)

        self.metadata.add_document(
            filename=filename,
            size_bytes=size_bytes,
            chunks=len(chunks),
            characters=len(cleaned_text),
            chat_id=chat_id,
        )

        return {
            "filename": filename,
            "size_bytes": size_bytes,
            "characters": len(cleaned_text),
            "chunks": len(chunks),
            "message": "Document indexed successfully."
        }