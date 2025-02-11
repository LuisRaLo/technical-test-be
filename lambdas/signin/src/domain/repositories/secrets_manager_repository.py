from abc import ABC, abstractmethod
from typing import Optional


class ISecretsManagerRepository(ABC):
    @abstractmethod
    def get_secret(self, secret_name: str) -> Optional[str | dict]:
        pass
