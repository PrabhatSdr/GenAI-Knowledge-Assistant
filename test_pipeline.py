from rag.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

response = pipeline.ask(
    "What is self-attention?"
)

print(response)