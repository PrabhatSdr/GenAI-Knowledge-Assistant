from services.embedding_service import EmbeddingService
from rag.vector_store import VectorStore


class RetrievalService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(self, query: str, limit: int = 3):

        # Convert question into embedding
        query_embedding = self.embedding_service.embed_text(query)

        # Search Qdrant
        results = self.vector_store.client.query_points(
            collection_name=self.vector_store.COLLECTION_NAME,
            query=query_embedding,
            limit=limit
        ).points

        retrieved_chunks = []

        for result in results:
            retrieved_chunks.append({
                "score": result.score,
                "text": result.payload["text"],
                "filename": result.payload["filename"],
                "chunk_id": result.payload["chunk_id"]
            })

        return retrieved_chunks