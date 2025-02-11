from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.domain.models.cognito import AuthenticationResult
from src.domain.enums.challenges_mfa_type import ChallengesMFATypeEnum


class SignInRequest(BaseModel):
    user: str = Field(..., min_length=1, description="The username to sign in")
    password: str = Field(
        ..., min_length=6, description="The password must be at least 6 characters long"
    )

    # Validación personalizada para el campo 'user'
    @field_validator("user")
    def user_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Username cannot be empty or just spaces")
        return v

    # Validación personalizada para el campo 'password'
    @field_validator("password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class SignInVerifyRequest(BaseModel):
    user: str = Field(..., min_length=1, description="The username to sign in")
    session: str = Field(..., description="The session to verify the MFA code")
    authenticator_code: str = Field(..., description="The MFA code to verify")

    @field_validator("user")
    def user_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Username cannot be empty or just spaces")
        return v

    @field_validator("authenticator_code")
    def authenticator_code_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Authenticator code cannot be empty or just spaces")
        return v

    @field_validator("session")
    def session_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Session cannot be empty or just spaces")
        return v


@dataclass
class SignInResult:
    authentication_result: Optional[AuthenticationResult] = None
    retry_attempts: Optional[int] = None


@dataclass
class SignInMFAResult:
    challenge_name: Optional[ChallengesMFATypeEnum]
    session: Optional[str]
    retry_attempts: Optional[int]


@dataclass
class SignInResponse:
    mensaje: str
    resultado: Optional[SignInResult | SignInMFAResult] = None
