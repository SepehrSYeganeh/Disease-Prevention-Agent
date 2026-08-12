from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    String,
    UniqueConstraint,
    BigInteger
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from datetime import date, datetime
from typing import Optional

from . import MedicalBase


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
    birthdate: Mapped[Optional[date]] = mapped_column(Date)
    sex: Mapped[Optional[str]] = mapped_column(String(1))
    is_pregnant: Mapped[Optional[bool]]

    personal_medical_history: Mapped[Optional[dict]] = mapped_column(JSONB)
    family_medical_history: Mapped[Optional[dict]] = mapped_column(JSONB)
    lifestyle_habits: Mapped[Optional[dict]] = mapped_column(JSONB)
    substance_use: Mapped[Optional[dict]] = mapped_column(JSONB)
    psychiatric_disorders: Mapped[Optional[dict]] = mapped_column(JSONB)
    medications_supplements: Mapped[Optional[dict]] = mapped_column(JSONB)
    clinical_data: Mapped[Optional[dict]] = mapped_column(JSONB)
