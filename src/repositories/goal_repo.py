from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.goal import GoalModel


class GoalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, description: str, target_amount: float, deadline: str = None) -> GoalModel:
        new_goal = GoalModel(
            description=description,
            target_amount=target_amount,
            deadline=deadline
        )
        self.db.add(new_goal)
        await self.db.commit()
        await self.db.refresh(new_goal)
        return new_goal

    async def get_active_goals(self):
        """Retorna metas que não estão concluídas nem canceladas."""
        query = select(GoalModel).where(GoalModel.status == "Em andamento")
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_progress(self, goal_id: int, amount_added: float):
        """Adiciona valor a uma meta específica."""
        query = select(GoalModel).where(GoalModel.id == goal_id)
        result = await self.db.execute(query)
        goal = result.scalar_one_or_none()
        if goal:
            goal.current_amount += amount_added
            # Verifica se atingiu a meta
            if goal.current_amount >= goal.target_amount:
                goal.status = "Concluído"
            await self.db.commit()
            await self.db.refresh(goal)
        return goal
