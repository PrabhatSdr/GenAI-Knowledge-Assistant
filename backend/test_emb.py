from services.embedding_service import EmbeddingService
from sklearn.metrics.pairwise import cosine_similarity

embedding_service = EmbeddingService()

text1 = "What is machine learning?"
text2 = "Explain machine learning."
text3 = "How do I bake a chocolate cake?"

emb1 = embedding_service.embed_text(text1)
emb2 = embedding_service.embed_text(text2)
emb3 = embedding_service.embed_text(text3)

print("Embedding Dimension:", len(emb1))

print(
    "Similarity (1 vs 2):",
    cosine_similarity([emb1], [emb2])[0][0]
)

print(
    "Similarity (1 vs 3):",
    cosine_similarity([emb1], [emb3])[0][0]
)