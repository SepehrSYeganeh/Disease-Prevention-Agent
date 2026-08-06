from pydantic import BaseModel, Field, model_validator
from typing import Literal, Any
from datetime import date, datetime
from uuid import UUID


class HealthProfile(BaseModel):
    """Base schema for user health profile."""
    id: UUID = Field(description="Primary key")
    created_at: datetime = Field(description="Date and time at which the user was created")
    first_name: str | None = Field(default=None, description="User's first name")
    last_name: str | None = Field(default=None, description="User's last name")
    birthdate: date | None = Field(default=None, le=date.today(), description="User's date of birth")
    sex: Literal['M', 'F', 'X'] | None = Field(default=None, description="Biological sex: M, F, or X")
    is_pregnant: bool | None = Field(default=None, description="Pregnancy status, if applicable")
    personal_medical_history: dict[str, Any] = Field(
        default_factory=dict,
        description="Personal medical history"
    )
    family_medical_history: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Family medical history"
    )
    lifestyle_habits: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Lifestyle and habits"
    )
    substance_use: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Substance use"
    )
    psychiatric_disorders: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Psychiatric disorders"
    )
    medications_supplements: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Medication supplements"
    )
    clinical_data: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Clinical data"
    )

    @model_validator(mode='after')
    def validate_pregnancy(self) -> 'HealthProfile':
        if self.is_pregnant and self.sex != 'F':
            raise ValueError("is_pregnant=True is only valid when sex is 'F'")
        return self


def select_profile(identifier: str) -> HealthProfile | None:
    ...


def insert_profile():
    ...


def update_profile():
    ...
