import os
import boto3

from src.application.resend_mfa import ResendMFAService
from src.application.confirm_mfa import ConfirmMFAService
from src.application.get_mfa_secret import GetMFASecretService
from src.application.confirm_sign_up_service import ConfirmSignUpService
from src.domain.repositories.secrets_manager_repository import (
    ISecretsManagerRepository,
)
from src.application.verify_mfa_token import VerifyMFATokenService
from src.application.sign_in_service import SignInService
from src.application.sign_up_service import SignUpService
from src.domain.repositories.cognito_repository import ICognitoRepository
from src.domain.models.sm_lambda_auth_cognito import SmLambdaAuthCognito
from src.infrastructure.utils.logger import CustomLogger
from src.infrastructure.repositories.cognito_repository_impl import (
    CognitoRepositoryImpl,
)
from src.infrastructure.repositories.secrets_manager_repository_impl import (
    SecretsManagerRepositoryImpl,
)


region = os.getenv("REGION")
sm_lambda_auth_cognito_secretname = os.getenv("SMLAMBDAAUTHORIZERCOGNITO")


def create_boto3_client(service_name: str, region: str):
    return boto3.Session().client(service_name, region_name=region)


sm_client = create_boto3_client("secretsmanager", region)
cognito_client = create_boto3_client("cognito-idp", region)


############ REPOSITORIES ############
def get_logger() -> CustomLogger:
    level_log = os.getenv("LOGLEVEL", "INFO")
    return CustomLogger(level_log=level_log)


def get_sm_repository() -> ISecretsManagerRepository:
    return SecretsManagerRepositoryImpl(
        sm_client=sm_client, secret_type=SmLambdaAuthCognito
    )


def cognito_repository() -> ICognitoRepository:
    sm_repository = get_sm_repository()
    sm_lambda_auth_cognito_value = sm_repository.get_secret(
        secret_name=sm_lambda_auth_cognito_secretname
    )

    return CognitoRepositoryImpl(
        logger=get_logger(),
        cognito_client=cognito_client,
        cognito_configs=sm_lambda_auth_cognito_value,
    )


############ SERVICES ############
def get_signin_service() -> SignInService:
    return SignInService(logger=get_logger(), cognito_repository=cognito_repository())


def get_verify_mfa_service() -> VerifyMFATokenService:
    return VerifyMFATokenService(
        logger=get_logger(), cognito_repository=cognito_repository()
    )


def get_signup_service() -> SignUpService:
    return SignUpService(logger=get_logger(), cognito_repository=cognito_repository())


def get_confirm_signup_service() -> ConfirmSignUpService:
    return ConfirmSignUpService(
        logger=get_logger(), cognito_repository=cognito_repository()
    )


def get_mfa_secret_service() -> GetMFASecretService:
    return GetMFASecretService(
        logger=get_logger(), cognito_repository=cognito_repository()
    )


def confirm_mfa_service() -> ConfirmMFAService:
    return ConfirmMFAService(
        logger=get_logger(), cognito_repository=cognito_repository()
    )


def get_resend_mfa_service() -> ResendMFAService:
    return ResendMFAService(
        logger=get_logger(), cognito_repository=cognito_repository()
    )
