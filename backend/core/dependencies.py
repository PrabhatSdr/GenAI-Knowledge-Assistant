from services.embedding_service import EmbeddingService
from rag.vector_store import VectorStore

# Load once
embedding_service = EmbeddingService()

# Connect once
vector_store = VectorStore()
vector_store.create_collection()