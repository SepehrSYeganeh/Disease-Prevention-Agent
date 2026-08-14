from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
    BigInteger,
    Integer,
    Numeric,
    func,
    select
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict, field_validator

from datetime import datetime
from typing import Optional, Literal

from . import MedicalBase, AsyncSession


class UserHealthProfile(MedicalBase):
    __tablename__ = "user_health_profile"

    __table_args__ = (
        UniqueConstraint("user_id", name="uq_user_health_profile_user_id"),
        CheckConstraint("sex IN ('M', 'F', 'X')", name="ck_user_health_profile_sex")
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("public.users.identifier", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    first_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[Optional[str]] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer)
    sex: Mapped[Optional[str]] = mapped_column(String(1))
    height: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    weight: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))


async def get_user_health_profile(identifier: str) -> Optional[UserHealthProfile]:
    async with AsyncSession() as session:
        result = await session.execute(
            select(UserHealthProfile).where(UserHealthProfile.user_id == identifier)
        )
        return result.scalar_one_or_none()


async def upsert_user_health_profile(
        identifier: str,
        **fields
) -> UserHealthProfile:
    async with AsyncSession() as session:
        stmt = insert(UserHealthProfile).values(user_id=identifier, **fields)
        stmt = stmt.on_conflict_do_update(
            index_elements=["user_id"],
            set_=fields,
        ).returning(UserHealthProfile)

        result = await session.execute(stmt)
        await session.commit()
        return result.scalar_one()


class HealthProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    created_at: datetime

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[Literal["M", "F", "X"]] = None
    height: Optional[float] = None
    weight: Optional[float] = None

    @field_validator("sex", mode="before")
    @classmethod
    def _validate_sex(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("M", "F", "X"):
            raise ValueError("sex must be one of 'M', 'F', 'X'")
        return v


async def user_health_profile_to_schema(orm_obj: UserHealthProfile) -> HealthProfileSchema:
    """Convert a UserHealthProfile SQLAlchemy instance into its Pydantic schema."""
    return HealthProfileSchema.model_validate(orm_obj)
