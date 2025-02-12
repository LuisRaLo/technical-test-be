from abc import ABC, abstractmethod
from typing import Any, Optional

from src.domain.models.cognito import CognitoInitiateAuth, CognitoInitiateAuthMFA


class ICognitoRepository(ABC):
    @abstractmethod
    def signin_with_email(
        email: str, password: str
    ) -> Optional[CognitoInitiateAuth | CognitoInitiateAuthMFA]:
        pass

    @abstractmethod
    def get_mfa_secret(access_token: str) -> Optional[str]:
        pass

    @abstractmethod
    def verify_mfa(
        mfa_code: str,
        access_token: Optional[str] = None,
        session: Optional[str] = None,
    ) -> Optional[bool | str]:
        pass

    @abstractmethod
    def software_token_auth_challenge(
        username: str, session: str, authenticator_code: str
    ):
        pass

    @abstractmethod
    def signup(email: str, password: str, name: str) -> Any:
        pass

    @abstractmethod
    def confirm_user_sign_up(user: str, confirmation_code: str) -> bool:
        pass

    @abstractmethod
    def resend_confirmation(user: str):
        pass

    @abstractmethod
    def set_user_mfa_preference(
        software_token_mfa_settings: dict,
        access_token: str,
    ) -> Any:
        pass
