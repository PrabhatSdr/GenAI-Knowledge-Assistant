from sentence_transformers import SentenceTransformer
from config.settings import settings


class EmbeddingService:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        print("Embedding model loaded successfully!")

    def embed_text(self, text: str):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def embed_query(self, query: str):
        """
        Generate embedding for a search query.
        """
        return self.embed_text(query)

    def embed_documents(self, documents: list[str]):
        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embeddings.tolist()