from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID


class BiometricLog(BaseModel):
    """Base schema for user biometric log."""
    id: UUID = Field(description="Primary key")
    recorded_at: datetime = Field(description="Timestamp of the record; cannot be in the future")
    height_cm: Optional[float | int] = Field(default=None, description="Height in centimeters")
    weight_kg: Optional[float | int] = Field(default=None, description="Weight in kilograms")
    bmi: Optional[float | int] = Field(default=None, description="BMI (computed); supply only when reading from DB")
    systolic_bp: Optional[int] = Field(default=None, description="Systolic blood pressure (mmHg)")
    diastolic_bp: Optional[int] = Field(default=None, description="Diastolic blood pressure (mmHg)")
    resting_hr: Optional[int] = Field(default=None, description="Resting heart rate (bpm)")
    blood_glucose: Optional[float | int] = Field(default=None, description="Blood glucose (mg/dL)")
    triglycerides: Optional[float | int] = Field(default=None, description="Triglycerides (mg/dL)")
    notes: Optional[Dict[str, Any]] = Field(default=None, description="Free-form JSONB notes")

    @field_validator('recorded_at')
    @classmethod
    def validate_recorded_at(cls, v: datetime) -> datetime:
        now = datetime.now(v.tzinfo or timezone.utc)
        if v > now:
            raise ValueError("recorded_at cannot be in the future")
        return v

    @field_validator('height_cm', 'weight_kg', 'blood_glucose', 'triglycerides')
    @classmethod
    def validate_positive(cls, v: Optional[float | int]) -> Optional[float | int]:
        if v is not None and v <= 0:
            raise ValueError("value must be greater than 0")
        return v

    @model_validator(mode='after')
    def compute_bmi(self) -> 'BiometricLog':
        if self.bmi is None and self.height_cm and self.weight_kg and self.height_cm > 0:
            h = self.height_cm / 100
            self.bmi = round(self.weight_kg / (h ** 2), 2)
        return self


def insert_biolog():
    ...


def update_biolog():
    ...


def select_biolog():
    pass
