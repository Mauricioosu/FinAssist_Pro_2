from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime
from src.core.database import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    # Valor (Positivo=Ganho, Negativo=Gasto)
    amount: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String, default="Geral")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_recurring: Mapped[bool] = mapped_column(default=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f"<Transaction(id={self.id}, desc={self.description}, amount={self.amount})>"
