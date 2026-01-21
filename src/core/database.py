import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Define o caminho do banco na pasta 'data' na raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # src/core
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "finassist_v2.db")

# Garante que a pasta data existe
os.makedirs(DATA_DIR, exist_ok=True)

# URL de Conexão SQLite (Driver aiosqlite para async)
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Engine (Motor do Banco)
engine = create_async_engine(
    DATABASE_URL,
    echo=False, # Mude para True se quiser ver os SQLs no terminal (debug)
    connect_args={"check_same_thread": False} # Necessário para SQLite
)

# Fábrica de Sessões
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Classe Base para os Modelos (Tabelas)
class Base(DeclarativeBase):
    pass

# Dependência para obter a sessão (Dependency Injection)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session