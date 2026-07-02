import ollama


def ask_llm(prompt: str, model: str = "llama3.2:3b") -> str:
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for academic research and learning."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"LLM Error: {str(e)}"