from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
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

    async def get_recent(self, limit: int = 10):
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