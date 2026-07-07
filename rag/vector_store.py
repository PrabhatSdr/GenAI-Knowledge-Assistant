from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

from config.settings import settings


class VectorStore:

    COLLECTION_NAME = "documents"

    def __init__(self):
        print("Connecting to Qdrant...")

        self.client = QdrantClient(
            path=settings.QDRANT_PATH
        )

        print("Connected to Qdrant successfully!")

    def create_collection(self):

        collections = self.client.get_collections().collections

        names = [collection.name for collection in collections]

        if self.COLLECTION_NAME in names:
            print("Collection already exists.")
            return

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

        print("Collection created successfully!")

    # 👇 ADD THIS NEW METHOD HERE
    def insert_documents(
        self,
        chunks: list[str],
        embeddings: list[list[float]],
        filename: str
    ):

        points = []

        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "text": chunk,
                        "filename": filename,
                        "chunk_id": index
                    }
                )
            )

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points
        )

        print(f"{len(points)} chunks stored successfully.")

    def close(self):
        self.client.close()