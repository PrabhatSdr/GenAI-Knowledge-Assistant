import requests

from config.settings import settings


class LLMService:

    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str):

        response = requests.post(
            self.base_url,
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()

        return response.json()["response"]