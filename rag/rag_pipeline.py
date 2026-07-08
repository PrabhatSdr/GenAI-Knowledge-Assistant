from services.retrieval_service import RetrievalService
from core.llm import LLMService
from core.prompts import SYSTEM_PROMPT


class RAGPipeline:

    def __init__(self):
        self.retriever = RetrievalService()
        self.llm = LLMService()

    def ask(self, question):

        retrieved_chunks = self.retriever.retrieve(question)

        context = "\n\n".join(
            [chunk["text"] for chunk in retrieved_chunks]
        )

        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question
        )

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": [
                {
                    "filename": chunk["filename"],
                    "chunk_id": chunk["chunk_id"],
                    "score": round(chunk["score"], 4),
                }
                for chunk in retrieved_chunks
            ],
        }