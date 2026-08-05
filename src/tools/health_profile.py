from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal, Dict, Any, Optional
from datetime import date, datetime
from uuid import UUID


class HealthProfile(BaseModel):
    """Base schema for user health profile."""
    id: UUID = Field(description="Primary key")
    created_at: datetime = Field(description="Date and time at which the user was created")
    first_name: Optional[str] = Field(default=None, description="User's first name")
    last_name: Optional[str] = Field(default=None, description="User's last name")
    birthdate: Optional[date] = Field(default=None, description="User's date of birth")
    sex: Optional[Literal['M', 'F', 'X']] = Field(default=None, description="Biological sex: M, F, or X")
    is_pregnant: Optional[bool] = Field(default=None, description="Pregnancy status, if applicable")
    personal_medical_history: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Personal medical history"
    )
    family_medical_history: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Family medical history"
    )
    lifestyle_habits: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Lifestyle and habits"
    )
    substance_use: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Substance use"
    )
    psychiatric_disorders: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Psychiatric disorders"
    )
    medications_supplements: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Medication supplements"
    )
    clinical_data: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Clinical data"
    )

    @field_validator('sex')
    @classmethod
    def validate_sex(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ('M', 'F', 'X'):
            raise ValueError("sex must be 'M', 'F', or 'X'")
        return v

    @field_validator('birthdate')
    @classmethod
    def validate_birthdate(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v > date.today():
            raise ValueError("birthdate cannot be in the future")
        return v

    @model_validator(mode='after')
    def validate_pregnancy(self) -> 'HealthProfile':
        if self.is_pregnant and self.sex != 'F':
            raise ValueError("is_pregnant=True is only valid when sex is 'F'")
        return self


def select_profile(identifier: str) -> Optional[HealthProfile]:
    ...


def insert_profile():
    ...


def update_profile():
    ...
