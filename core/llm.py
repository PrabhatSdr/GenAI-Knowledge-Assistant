import json
import requests

from config.settings import settings


class LLMService:

    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"

    # -----------------------------------------
    # Normal Response (already used)
    # -----------------------------------------
    def generate(self, prompt: str):

        response = requests.post(
            self.base_url,
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
        )

        response.raise_for_status()

        return response.json()["response"]

    # -----------------------------------------
    # Streaming Response (NEW)
    # -----------------------------------------
    def generate_stream(self, prompt: str):

        response = requests.post(
            self.base_url,
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": True,
            },
            stream=True,
        )

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            data = json.loads(line.decode("utf-8"))

            if "response" in data:
                yield data["response"]

            if data.get("done", False):
                break