import httpx


class OllamaProvider:
    def __init__(self, model="llama3:8b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    async def generate(self, system_prompt: str, user_query: str) -> str:
        """
        Envia o prompt para o modelo local e retorna o texto puro.
        Configurado com temperatura baixa para evitar alucinações matemáticas.
        """
        prompt_completo = f"{system_prompt}\n\nUSER: {user_query}"
        payload = {
            "model": self.model,
            "prompt": prompt_completo,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Muito baixa para ser preciso
                "num_ctx": 4096      # Contexto maior para ler histórico
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
