from abc import ABC, abstractmethod
from typing import Optional

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
