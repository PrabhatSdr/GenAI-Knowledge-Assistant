import os

from rag.document_loader import DocumentLoader
from rag.text_cleaner import TextCleaner
from rag.chunker import TextChunker

from services.embedding_service import EmbeddingService
from core.database import vector_store


class IngestionService:

    def __init__(self):
        # Initialize helper classes
        self.loader = DocumentLoader()
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()
        self.embedder = EmbeddingService()

        # Ensure Qdrant collection exists
        vector_store.create_collection()

    def ingest(self, file_path: str):

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
            filename=filename
        )

        print("Document stored successfully!")
        print("=" * 60)

        return {
            "filename": filename,
            "characters": len(cleaned_text),
            "chunks": len(chunks),
            "message": "Document indexed successfully."
        }