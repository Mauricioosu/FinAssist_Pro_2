import asyncio
from src.core.database import engine, Base


async def init_models():
    async with engine.begin() as conn:
        print("Criando tabelas no banco de dados...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Banco de dados 'finassist_v2.db' pronto!")

if __name__ == "__main__":
    asyncio.run(init_models())
