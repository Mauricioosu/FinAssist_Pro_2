import json
import re
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.finance_engine import FinanceEngine
from src.ai.provider import OllamaProvider

class AIController:
    def __init__(self, session: AsyncSession):
        self.engine = FinanceEngine(session)
        self.provider = OllamaProvider()
        
        # PROMPT DE SISTEMA OTIMIZADO PARA AÇÃO
        self.system_prompt = """
        Você é o FinAssist Pro 2, um assistente financeiro pessoal e privado.
        
        SEU OBJETIVO:
        1. Analisar o CONTEXTO FINANCEIRO abaixo.
        2. Responder dúvidas ou EXECUTAR AÇÕES (registros).

        REGRAS CRÍTICAS:
        - NÃO invente dados. Use apenas o que está no CONTEXTO.
        - Se o usuário quiser REGISTRAR algo (gasto, ganho, meta), você NÃO deve apenas falar "ok". 
        - Você deve emitir um COMANDO JSON no final da resposta.

        FORMATO DE COMANDO (JSON):
        Para transações:
        <<<{"action": "transaction", "desc": "Compra de X", "val": -50.00, "cat": "Lazer"}>>>
        
        Para metas:
        <<<{"action": "goal", "desc": "Viagem", "target": 5000.00, "deadline": "Dez/2026"}>>>

        Exemplo de Resposta:
        "Entendido! Registrei seu almoço."
        <<<{"action": "transaction", "desc": "Almoço", "val": -35.00, "cat": "Alimentação"}>>>
        """

    async def process_query(self, user_query: str) -> str:
        # 1. Obter o contexto atualizado do banco de dados
        contexto_financeiro = await self.engine.generate_dashboard_context()
        
        # 2. Montar o prompt final
        full_prompt = f"{self.system_prompt}\n\n### CONTEXTO FINANCEIRO ATUAL ###\n{contexto_financeiro}"
        
        # 3. Chamar a IA
        raw_response = await self.provider.generate(full_prompt, user_query)
        
        # 4. Processar Intent (Procurar JSON de ação)
        final_response = await self._handle_actions(raw_response)
        
        return final_response

    async def _handle_actions(self, response_text: str) -> str:
        """Busca e executa blocos JSON delimitados por <<< >>>"""
        pattern = r"<<<(.*?)>>>"
        match = re.search(pattern, response_text, re.DOTALL)
        
        if match:
            try:
                json_str = match.group(1)
                data = json.loads(json_str)
                clean_text = response_text.replace(match.group(0), "").strip()
                
                # Executa a ação no Engine
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