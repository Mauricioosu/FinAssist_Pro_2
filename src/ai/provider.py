import httpx
from src.config import settings


class OllamaProvider:
    def __init__(self):
        self.model = settings.OLLAMA_MODEL
        self.api_url = settings.OLLAMA_API_URL

    async def generate(self, system_prompt: str, user_query: str) -> str:
        """
        Envia o prompt para o modelo local e retorna o texto puro.
        """
        prompt_completo = f"{system_prompt}\n\nUSER: {user_query}"
        payload = {
            "model": self.model,
            "prompt": prompt_completo,
            "stream": False,
            "options": {
                "temperature": settings.OLLAMA_TEMPERATURE,
                "num_ctx": settings.OLLAMA_CONTEXT_WINDOW
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.api_url, json=payload, timeout=60.0)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
                else:
                    return f"Erro: Ollama retornou código {response.status_code}"
            except Exception as e:
                return f"Erro de conexão: O Ollama está rodando? Detalhes: {e}"
