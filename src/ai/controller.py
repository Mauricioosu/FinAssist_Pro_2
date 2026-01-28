import re
from sqlalchemy.ext.asyncio import AsyncSession
from json_repair import repair_json
from src.services.finance_engine import FinanceEngine
from src.ai.provider import OllamaProvider
from src.config import settings
import plotly.graph_objects as go
import chainlit as cl


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
        """
        Busca e executa blocos JSON.
        Agora usa json_repair para tolerar erros de sintaxe da IA.
        """
        pattern = r"<<<(.*?)>>>"
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            try:
                json_str = match.group(1)
                # BLINDAGEM: Usa repair_json para corrigir vírgulas extras, aspas faltando, etc.
                data = repair_json(json_str, return_objects=True)
                # Remove o JSON técnico da resposta final para o usuário
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

                elif data.get("action") == "chart":
                    raw_data = await self.engine.transaction_repo.get_expenses_by_category()

                    if not raw_data:
                        return f"{clean_text}\n\n⚠️ *Não encontrei gastos para gerar o gráfico.*"

                    labels = [row[0] for row in raw_data]
                    values = [abs(row[1]) for row in raw_data]
                    # Cria o objeto Gráfico de Rosca
                    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
                    fig.update_layout(title_text="Distribuição de Gastos por Categoria")
                    # Envia o gráfico como um Elemento do Chainlit
                    elements = [cl.Plotly(name="gastos", figure=fig, display="inline")]
                    await cl.Message(content="Aqui está a visualização dos seus gastos:", elements=elements).send()

                    return f"{clean_text}\n\n📊 *Gráfico gerado com sucesso!*"

                elif data.get("action") == "report":
                    mes = int(data.get("month"))
                    ano = int(data.get("year"))
                    transactions = await self.engine.transaction_repo.get_monthly_transactions(mes, ano)
                    if not transactions:
                        return f"{clean_text}\n\n⚠️ *Não encontrei transações em {mes}/{ano}.*"

                    # Calcula totais na memória (rápido e simples)
                    ganhos = sum(t.amount for t in transactions if t.amount > 0)
                    gastos = sum(t.amount for t in transactions if t.amount < 0)
                    saldo_periodo = ganhos + gastos

                    # Monta a resposta formatada
                    report = [f"📅 **Relatório de {mes}/{ano}**\n"]
                    report.append(f"🟢 Entradas: R$ {ganhos:.2f}")
                    report.append(f"🔴 Saídas:   R$ {gastos:.2f}")
                    report.append(f"💰 Resultado: R$ {saldo_periodo:.2f}\n")
                    report.append("**Detalhamento:**")
                    for t in transactions:
                        sinal = "+" if t.amount >= 0 else ""
                        dt = t.created_at.strftime('%d/%m')
                        report.append(f"- {dt}: {t.description} ({sinal}R$ {t.amount:.2f})")

                    return f"{clean_text}\n\n" + "\n".join(report)
            except Exception as e:
                # Se mesmo o repair falhar, avisa o usuário sem travar o app
                return f"{response_text}\n\n⚠️ *Não consegui processar a ação. Erro: {str(e)}*"
        return response_text
