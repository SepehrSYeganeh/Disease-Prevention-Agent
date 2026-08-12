from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

import uuid
from datetime import datetime
from typing import Any

from . import MedicalBase


class BiometricLog(MedicalBase):
    __tablename__ = "user_biometric_log"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_health_profile.id", ondelete="CASCADE"),
        nullable=False,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    height_cm: Mapped[float | None] = mapped_column(Numeric(5, 2), default=None)
    weight_kg: Mapped[float | None] = mapped_column(Numeric(5, 2), default=None)
    bmi: Mapped[float | None] = mapped_column(Numeric(4, 2), default=None)

    systolic_bp: Mapped[int | None] = mapped_column(Integer, default=None)
    diastolic_bp: Mapped[int | None] = mapped_column(Integer, default=None)
    resting_hr: Mapped[int | None] = mapped_column(Integer, default=None)

    blood_glucose: Mapped[float | None] = mapped_column(Numeric(5, 2), default=None)
    triglycerides: Mapped[float | None] = mapped_column(Numeric(5, 2), default=None)

    notes: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
