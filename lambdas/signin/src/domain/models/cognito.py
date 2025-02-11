from pydantic import BaseModel

from src.domain.enums.challenges_mfa_type import ChallengesMFATypeEnum


class CognitoChallengeParameters(BaseModel):
    USER_ID_FOR_SRP: str


class ResponseMetadataHeaders(BaseModel):
    DATE: str
    CONTENT_TYPE: str
    CONSTENT_LENGTH: str
    CONNECTION: str
    X_AMZN_REQUESTID: str


class ResponseMetadata(BaseModel):
    REQUEST_ID: str
    HTTP_STATUS_CODE: int
    HTTP_HEADERS: ResponseMetadataHeaders
    RETRY_ATTEMPS: int


class CognitoInitiateAuthMFA(BaseModel):
    CHALLENGE_NAME: ChallengesMFATypeEnum
    SESSION: str
    CHALLENGE_PARAMETERS: CognitoChallengeParameters
    RESPONSE_METADATA: ResponseMetadata


class AuthenticationResult(BaseModel):
    ID_TOKEN: str
    REFRESH_TOKEN: str
    ACCESS_TOKEN: str
    EXPIRES_IN: int
    TOKEN_TYPE: str


class CognitoInitiateAuth(BaseModel):
    CHALLENGE_PARAMETERS: CognitoChallengeParameters
    AUTHENTICATION_RESULT: AuthenticationResult
    RESPONSE_METADATA: ResponseMetadata
