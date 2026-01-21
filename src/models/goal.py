from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime
from src.core.database import Base

class GoalModel(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    target_amount: Mapped[float] = mapped_column(Float) # Valor Alvo
    current_amount: Mapped[float] = mapped_column(Float, default=0.0) # Valor Guardado
    deadline: Mapped[str | None] = mapped_column(String, nullable=True) # Ex: "Dez/2026"
    status: Mapped[str] = mapped_column(String, default="Em andamento")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Goal(desc={self.description}, target={self.target_amount})>"