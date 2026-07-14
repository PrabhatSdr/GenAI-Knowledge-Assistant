from services.embedding_service import EmbeddingService
from core.database import vector_store


class RetrievalService:

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def retrieve(self, query, top_k=5):

        query_embedding = self.embedding_service.embed_query(query)

        results = vector_store.search(
            query_embedding=query_embedding,
            limit=top_k
        )

        retrieved = []

        for point in results:

            retrieved.append(
                {
                    "text": point.payload["text"],
                    "filename": point.payload["filename"],
                    "chunk_id": point.payload["chunk_id"],
                    "score": point.score,
                }
            )

        return retrieved