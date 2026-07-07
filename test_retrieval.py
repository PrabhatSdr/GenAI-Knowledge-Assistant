from services.retrieval_service import RetrievalService

retriever = RetrievalService()

results = retriever.retrieve(
    "What are transformers?"
)

print("\nRetrieved Results:\n")

for index, result in enumerate(results, start=1):
    print("=" * 60)
    print(f"Result {index}")
    print(f"Score: {result['score']:.4f}")
    print(f"Filename: {result['filename']}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Text: {result['text']}")