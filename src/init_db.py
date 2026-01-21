import asyncio
from src.core.database import engine, Base
# Importar os modelos para que o SQLAlchemy os reconheça
from src.models.transaction import TransactionModel

async def init_models():
    async with engine.begin() as conn:
        # Apaga tudo e recria (CUIDADO em produção! Use apenas em DEV)
        # await conn.run_sync(Base.metadata.drop_all) 
        
        print("Criando tabelas no banco de dados...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Banco de dados 'finassist_v2.db' pronto!")

if __name__ == "__main__":
    asyncio.run(init_models())