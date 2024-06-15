from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
import asyncio
import os
DATABASE_URL = f"postgresql+asyncpg://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
	engine, class_=AsyncSession, expire_on_commit=False
)
async def init_models():
	
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

# Dependency
async def get_session() -> AsyncSession:
	async with async_session() as session:
		yield session