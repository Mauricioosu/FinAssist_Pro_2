import asyncio
from src.core.database import get_db, engine
from src.models.transaction import Base
from src.services.finance_engine import FinanceEngine

async def main():
    # 1. Resetar banco para teste limpo (opcional)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Iniciar Sessão e Motor
    async for session in get_db():
        engine_service = FinanceEngine(session)

        print("--- TESTE 1: Inserindo Dados ---")
        saldo = await engine_service.add_new_transaction("Salário", 5000.00, "Renda")
        print(f"Salário recebido. Saldo: {saldo}")
        
        await engine_service.add_new_transaction("Almoço", -45.50, "Alimentação")
        await engine_service.add_new_transaction("Uber", -22.00, "Transporte")
        print("Gastos registrados.")

        print("\n--- TESTE 2: Gerando Contexto para IA ---")
        contexto = await engine_service.generate_dashboard_context()
        print(contexto)
        
        break # Fecha o loop do gerador

if __name__ == "__main__":
    asyncio.run(main())