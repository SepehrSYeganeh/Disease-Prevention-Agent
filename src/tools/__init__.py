from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os

engine = create_async_engine(os.getenv('DATABASE_URL'), echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
