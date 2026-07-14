from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

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
        """
        Create the collection if it does not already exist.
        """

        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.COLLECTION_NAME in collection_names:
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

    def add_documents(self, chunks, embeddings, filename):
        """
        Store all document chunks into Qdrant.
        """

        points = []

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "filename": filename,
                    "chunk_id": i
                }
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points
        )

        print(f"{len(points)} chunks stored successfully!")

    def search(self, query_embedding, limit=5):
        """
        Retrieve the most similar chunks.
        """

        results = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_embedding,
            limit=limit
        )

        return results.points

    def delete_collection(self):
        """
        Delete the collection.
        Useful during development.
        """

        self.client.delete_collection(
            collection_name=self.COLLECTION_NAME
        )

        print("Collection deleted successfully!")

    def close(self):
        """
        Close the Qdrant connection.
        """

        self.client.close()