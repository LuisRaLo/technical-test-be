from dataclasses import dataclass
from typing import Optional


@dataclass
class MFASecret:
    secret: str


@dataclass
class MFASecretResponse:
    mensaje: str
    resultado: Optional[MFASecret] = None
