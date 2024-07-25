from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Create an asynchronous database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory for managing asynchronous sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Declare a base class for model definitions
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
        await session.commit()
