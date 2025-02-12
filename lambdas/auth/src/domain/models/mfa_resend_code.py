from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.domain.models.cognito import AuthenticationResult, CognitoChallengeParameters
from src.domain.enums.challenges_mfa_type import ChallengesMFATypeEnum


class ResendRequest(BaseModel):
    user: str = Field(..., min_length=1, description="The username to sign in")

    @field_validator("user")
    def user_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Username cannot be empty or just spaces")
        return v
