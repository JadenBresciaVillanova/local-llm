# backend/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://myuser:supersecret@rag_postgres/rag_db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False) # No need to echo sync calls
SyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine
)

# Helper to get a sync session
def get_sync_db_session():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()