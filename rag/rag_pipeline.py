from services.retrieval_service import RetrievalService
from core.llm import LLMService
from core.prompts import SYSTEM_PROMPT
from core.memory import memory


class RAGPipeline:

    def __init__(self):
        self.retriever = RetrievalService()
        self.llm = LLMService()

    def ask(self, question: str, chat_id: str = "default"):

        # -------------------------
        # Load previous history
        # -------------------------

        history = memory.get_history(chat_id)

        history_text = ""

        for message in history:
            history_text += (
                f"{message['role']}: {message['content']}\n"
            )

        # -------------------------
        # Retrieve documents
        # -------------------------

        retrieved_chunks = self.retriever.retrieve(question)

        context = "\n\n".join(
            chunk["text"] for chunk in retrieved_chunks
        )

        # -------------------------
        # Build prompt
        # -------------------------

        prompt = f"""
Previous Conversation:

{history_text}

Knowledge Base:

{context}

User Question:

{question}

Answer naturally.
"""

        # -------------------------
        # Generate answer
        # -------------------------

        answer = self.llm.generate(prompt)

        # -------------------------
        # Save conversation
        # -------------------------

        memory.add(chat_id, "user", question)
        memory.add(chat_id, "assistant", answer)

        # -------------------------
        # Return response
        # -------------------------

        return {
            "answer": answer,
            "sources": [
                {
                    "filename": chunk["filename"],
                    "chunk_id": chunk["chunk_id"],
                    "score": round(chunk["score"], 4)
                }
                for chunk in retrieved_chunks
            ]
        }