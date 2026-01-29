import httpx
from src.config import settings


http_client = httpx.AsyncClient(timeout=60.0)


class OllamaProvider:
    def __init__(self):
        self.model = settings.OLLAMA_MODEL
        self.api_url = settings.OLLAMA_API_URL

    async def generate(self, system_prompt: str, user_query: str) -> str:
        prompt_completo = f"{system_prompt}\n\nUSER: {user_query}"
        payload = {
            "model": self.model,
            "prompt": prompt_completo,
            "stream": False,
            "options": {
                "temperature": settings.OLLAMA_TEMPERATURE,
                "num_ctx": 4096
            },
            "keep_alive": "5m"
        }

        try:
            response = await http_client.post(self.api_url, json=payload)

            if response.status_code == 200:
                return response.json().get("response", "")
            return f"Erro Ollama: {response.status_code}"
        except Exception as e:
            return f"Erro de conexão local: {e}"
