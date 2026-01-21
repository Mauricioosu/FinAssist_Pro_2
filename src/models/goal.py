from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, DateTime
from src.core.database import Base


class GoalModel(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    # Valor Alvo
    target_amount: Mapped[float] = mapped_column(Float)
    # Valor Guardado
    current_amount: Mapped[float] = mapped_column(Float, default=0.0)
    deadline: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="Em andamento")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Goal(desc={self.description}, target={self.target_amount})>"
