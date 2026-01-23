import json
import re
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.finance_engine import FinanceEngine
from src.ai.provider import OllamaProvider
from src.config import settings


class AIController:
    def __init__(self, session: AsyncSession):
        self.engine = FinanceEngine(session)
        self.provider = OllamaProvider()
        self.system_prompt = settings.SYSTEM_PROMPT

    async def process_query(self, user_query: str) -> str:
        contexto_financeiro = await self.engine.generate_dashboard_context()
        full_prompt = f"{self.system_prompt}\n\n### CONTEXTO FINANCEIRO ATUAL ###\n{contexto_financeiro}"
        raw_response = await self.provider.generate(full_prompt, user_query)
        final_response = await self._handle_actions(raw_response)
        return final_response

    async def _handle_actions(self, response_text: str) -> str:
        """Busca e executa blocos JSON delimitados por <<< >>>"""
        # Nota: A lógica de parsing será o foco da próxima melhoria (Ação 3)
        pattern = r"<<<(.*?)>>>"
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            try:
                json_str = match.group(1)
                data = json.loads(json_str)
                clean_text = response_text.replace(match.group(0), "").strip()
                if data.get("action") == "transaction":
                    novo_saldo = await self.engine.add_new_transaction(
                        description=data.get("desc"),
                        amount=float(data.get("val")),
                        category=data.get("cat", "Geral")
                    )
                    return f"{clean_text}\n\n✅ *Transação salva! Novo Saldo: R$ {novo_saldo:.2f}*"
                elif data.get("action") == "goal":
                    await self.engine.goal_repo.create(
                        description=data.get("desc"),
                        target_amount=float(data.get("target")),
                        deadline=data.get("deadline")
                    )
                    return f"{clean_text}\n\n🎯 *Meta criada com sucesso!*"
            except Exception as e:
                return f"{response_text}\n\n⚠️ *Erro ao processar ação automática: {str(e)}*"
        return response_text
