from sentence_transformers import SentenceTransformer
from config.settings import settings


class EmbeddingService:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        print("Embedding model loaded successfully!")

    def embed_text(self, text):

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def embed_query(self, query):

        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embedding.tolist()

    def embed_documents(self, documents):

        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embeddings.tolist()