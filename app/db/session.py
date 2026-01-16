from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the Async Engine
# echo=True will log SQL queries to the console
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create the Session Factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Dependency to get DB session in endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()