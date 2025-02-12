from dataclasses import dataclass
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class SignUpRequest(BaseModel):
    email: str = Field(..., description="The email to sign up")
    password: str = Field(
        ..., min_length=6, description="The password must be at least 6 characters long"
    )
    repeat_password: str = Field(
        ..., min_length=6, description="The password must be at least 6 characters long"
    )
    name: str = Field(..., description="The name of the user")

    @field_validator("email")
    def email_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Email cannot be empty or just spaces")
        return v

    @field_validator("password", "repeat_password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or just spaces")
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.repeat_password:
            raise ValueError("Passwords do not match")
        return self


class ConfirmSignUpRequest(BaseModel):
    user: str = Field(..., description="The email to confirm")
    confirmation_code: str = Field(..., description="The confirmation code")

    @field_validator("user")
    def user_not_empty(cls, v):
        if not v.strip():
            raise ValueError("User cannot be empty or just spaces")
        return v

    @field_validator("confirmation_code")
    def confirmation_code_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Confirmation code cannot be empty or just spaces")
        return v


@dataclass
class SignUpResponse:
    mensaje: str
    resultado: Optional[Any] = None
