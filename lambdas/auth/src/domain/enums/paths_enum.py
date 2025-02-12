from enum import Enum


class PathsEnum(Enum):
    sign_in = "/auth/signin"
    sign_up = "/auth/signup"
    mfa_verify = "/auth/mfa/verify"
    mfa_code = "/auth/mfa/code"
    mfa_challenge = "/auth/mfa/challenge"
