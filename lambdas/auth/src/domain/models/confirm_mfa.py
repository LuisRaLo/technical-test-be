from dataclasses import dataclass
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


class ConfirmMFARequest(BaseModel):
    mfa_code: str = Field(..., description="The MFA code to confirm")
    access_token: str = Field(
        ..., description="The access token to confirm the MFA code"
    )
    session: Optional[str] = Field(
        None, description="The session token to confirm the MFA code"
    )

    @field_validator("mfa_code")
    def mfa_code_not_empty(cls, v):
        if not v.strip():
            raise ValueError("MFA code cannot be empty or just spaces")
        return v

    @field_validator("access_token")
    def access_token_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Access token cannot be empty or just spaces")
        return v


@dataclass
class ConfirmMFAResponse:
    mensaje: str
    resultado: Optional[Any] = None
