from services.retrieval_service import RetrievalService
from core.llm import LLMService
from core.prompts import SYSTEM_PROMPT
from core.memory import memory


class RAGPipeline:

    def __init__(self):
        self.retriever = RetrievalService()
        self.llm = LLMService()

    def ask(self, question):

        # -----------------------------
        # Save User Message
        # -----------------------------
        memory.add_user_message(question)

        # -----------------------------
        # Retrieve Relevant Chunks
        # -----------------------------
        retrieved_chunks = self.retriever.retrieve(question)

        # -----------------------------
        # Build Context
        # -----------------------------
        context = "\n\n".join(
            [
                chunk["text"]
                for chunk in retrieved_chunks
            ]
        )

        # -----------------------------
        # Build Conversation History
        # -----------------------------
        history = "\n".join(
            [
                f"{msg['role']}: {msg['content']}"
                for msg in memory.get_history()
            ]
        )

        # -----------------------------
        # Build Prompt
        # -----------------------------
        prompt = SYSTEM_PROMPT.format(
            context=context,
            history=history,
            question=question
        )

        # -----------------------------
        # Generate Answer
        # -----------------------------
        answer = self.llm.generate(prompt)

        # -----------------------------
        # Save AI Response
        # -----------------------------
        memory.add_ai_message(answer)

        # -----------------------------
        # Print Conversation Memory
        # -----------------------------
        print("\n========== Conversation Memory ==========")

        for msg in memory.get_history():
            print(f"{msg['role']}: {msg['content']}")

        print("=========================================\n")

        # -----------------------------
        # Return Response
        # -----------------------------
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