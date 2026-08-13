from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, DateTime
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    pool_pre_ping=True,
)

AsyncSession = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


class MedicalBase(DeclarativeBase):
    metadata = MetaData(schema="medical")
    type_annotation_map = {datetime: DateTime(timezone=True)}
