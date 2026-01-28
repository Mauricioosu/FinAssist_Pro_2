from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, extract
from src.models.transaction import TransactionModel


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, description: str, amount: float, category: str = "Geral") -> TransactionModel:
        """Cria uma nova transação e salva no banco."""
        transaction = TransactionModel(
            description=description,
            amount=amount,
            category=category
        )
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction

    async def get_recent(self, limit: int = 15):
        """Busca as últimas X transações para contexto da IA."""
        query = select(TransactionModel).order_by(TransactionModel.id.desc()).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_balance(self) -> float:
        """Calcula o saldo total somando todas as transações."""
        query = select(func.sum(TransactionModel.amount))
        result = await self.db.execute(query)
        balance = result.scalar()
        return balance if balance else 0.0

    async def get_totals(self):
        """
        Retorna tupla (Total Ganhos, Total Gastos).
        Usado no resumo do Dashboard.
        """
        # Soma Ganhos (> 0)
        query_in = select(func.sum(TransactionModel.amount)).where(TransactionModel.amount > 0)
        result_in = await self.db.execute(query_in)
        income = result_in.scalar() or 0.0

        # Soma Gastos (< 0)
        query_out = select(func.sum(TransactionModel.amount)).where(TransactionModel.amount < 0)
        result_out = await self.db.execute(query_out)
        expense = result_out.scalar() or 0.0

        return income, expense

    async def get_expenses_by_category(self):
        """
        [OPÇÃO A] Agrupa gastos por categoria para o gráfico.
        """
        query = (
            select(TransactionModel.category, func.sum(TransactionModel.amount))
            .where(TransactionModel.amount < 0)  # Apenas gastos
            .group_by(TransactionModel.category)
        )
        result = await self.db.execute(query)
        return result.all()

    async def get_monthly_transactions(self, month: int, year: int):
        """
        [OPÇÃO B] Busca todas as transações de um mês/ano específico.
        """
        query = (
            select(TransactionModel)
            .where(
                extract('month', TransactionModel.created_at) == month,
                extract('year', TransactionModel.created_at) == year
            )
            .order_by(TransactionModel.created_at.asc())
        )
        result = await self.db.execute(query)
        return result.scalars().all()
