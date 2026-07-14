from services.retrieval_service import RetrievalService
from core.llm import LLMService
from core.prompts import SYSTEM_PROMPT
from core.memory import memory


class RAGPipeline:

    def __init__(self):
        self.retriever = RetrievalService()
        self.llm = LLMService()

    def ask(self, question):

        # ----------------------------
        # Retrieve relevant chunks
        # ----------------------------
        retrieved_chunks = self.retriever.retrieve(question)

        context = "\n\n".join(
            [
                chunk["text"]
                for chunk in retrieved_chunks
            ]
        )

        # ----------------------------
        # Get conversation history
        # ----------------------------
        conversation = memory.get_history()

        # ----------------------------
        # Create prompt
        # ----------------------------
        prompt = SYSTEM_PROMPT.format(
            conversation=conversation,
            context=context,
            question=question
        )

        # ----------------------------
        # Generate answer
        # ----------------------------
        answer = self.llm.generate(prompt)

        # ----------------------------
        # Save conversation
        # ----------------------------
        memory.add_message("user", question)

        memory.add_message("assistant", answer)

        # ----------------------------
        # Build citations
        # ----------------------------
        citations = []

        for chunk in retrieved_chunks:

            citations.append(
                f"{chunk['filename']} (Chunk {chunk['chunk_id']})"
            )

        # Remove duplicates
        citations = list(dict.fromkeys(citations))

        return {
            "answer": answer,

            "citations": citations,

            "sources": [
                {
                    "filename": chunk["filename"],
                    "chunk_id": chunk["chunk_id"],
                    "score": round(chunk["score"], 4)
                }
                for chunk in retrieved_chunks
            ]
        }