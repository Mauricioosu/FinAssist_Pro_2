from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.transaction_repo import TransactionRepository
from src.repositories.goal_repo import GoalRepository


class FinanceEngine:
    def __init__(self, session: AsyncSession):
        self.transaction_repo = TransactionRepository(session)
        self.goal_repo = GoalRepository(session)

    async def add_new_transaction(self, description: str, amount: float, category: str):
        """
        Registra uma transação e retorna o novo saldo.
        A IA chama isso quando o usuário diz: "Gastei 50 em pizza".
        """
        # Registrar a transação
        await self.transaction_repo.create(description, amount, category)
        # Calcular impacto imediato (novo saldo)
        new_balance = await self.transaction_repo.get_balance()
        return new_balance

    async def generate_dashboard_context(self) -> str:
        """
        Gera relatório com Saldo, Resumo (Entradas/Saídas), Extrato e Metas.
        """
        # Busca dados
        balance = await self.transaction_repo.get_balance()
        income, expenses = await self.transaction_repo.get_totals()
        recent_tx = await self.transaction_repo.get_recent(limit=15)
        goals = await self.goal_repo.get_active_goals()
        # Monta o texto
        text_lines = []
        text_lines.append("📊 **RESUMO FINANCEIRO**")
        text_lines.append(f"💰 SALDO ATUAL:   R$ {balance:.2f}")
        text_lines.append(f"📈 TOTAL GANHO:   R$ {income:.2f}")
        text_lines.append(f"📉 TOTAL GASTO:   R$ {expenses:.2f}")
        text_lines.append("\n📝 **EXTRATO RECENTE:**")

        if not recent_tx:
            text_lines.append("- Nenhuma transação recente.")
        for tx in recent_tx:
            sinal = "+" if tx.amount >= 0 else ""
            data_fmt = tx.created_at.strftime('%d/%m')
            text_lines.append(f"- {data_fmt}: {tx.description} ({sinal}R$ {tx.amount:.2f}) [{tx.category}]")

        text_lines.append("\n🎯 **METAS ATIVAS:**")
        if not goals:
            text_lines.append("- Nenhuma meta definida.")
        for g in goals:
            if g.target_amount > 0:
                progresso = (g.current_amount / g.target_amount) * 100
            else:
                progresso = 0.0
            text_lines.append(f"- {g.description}: R$ {g.current_amount:.2f} de R$ {g.target_amount:.2f} ({progresso:.1f}%)")

        return "\n".join(text_lines)
