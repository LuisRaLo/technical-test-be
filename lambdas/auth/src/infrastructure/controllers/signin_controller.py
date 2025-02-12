from fastapi import APIRouter, Depends, Request, Response

from src.application.confirm_mfa import ConfirmMFAService
from src.domain.models.confirm_mfa import ConfirmMFARequest, ConfirmMFAResponse
from src.application.get_mfa_secret import GetMFASecretService
from src.domain.models.mfa_secret import MFASecretResponse
from src.infrastructure.utils.logger import CustomLogger

from src.domain.enums.paths_enum import PathsEnum
from src.domain.models.sign_in import SignInRequest, SignInResponse, SignInVerifyRequest
from src.application.sign_in_service import SignInService
from src.application.verify_mfa_token import VerifyMFATokenService
from src.application.services import (
    confirm_mfa_service,
    get_logger,
    get_mfa_secret_service,
    get_signin_service,
    get_verify_mfa_service,
)

router = APIRouter()


@router.post(
    PathsEnum.sign_in.value,
    response_model=SignInResponse,
    responses={
        200: {"model": SignInResponse, "description": "login is successfully"},
    },
)
async def signin(
    payload: SignInRequest,
    response: Response,
    signin_service: SignInService = Depends(get_signin_service),
    logger: CustomLogger = Depends(get_logger),
):
    logger.info(
        "Init Proccess",
        extra={"path": "POST /auth/signin", "payload": payload},
    )

    proccess = signin_service.execute(payload)

    response.status_code = proccess.statusCode

    logger.info(
        "Proccess is finished",
        extra={"statusCode": proccess.statusCode, "response": proccess.result},
    )

    return proccess.result


@router.post(
    PathsEnum.mfa_verify.value,
    response_model=SignInResponse,
    responses={
        200: {"model": SignInResponse, "description": "login is successfully"},
    },
)
async def verify_mfa(
    response: Response,
    payload: SignInVerifyRequest,
    verify_mfa_service: VerifyMFATokenService = Depends(get_verify_mfa_service),
    logger: CustomLogger = Depends(get_logger),
):
    logger.info(
        "Init Proccess",
        extra={"path": "POST /auth/mfa/verify", "payload": payload},
    )

    proccess = verify_mfa_service.execute(payload)

    response.status_code = proccess.statusCode

    logger.info(
        "Proccess is finished",
        extra={"statusCode": proccess.statusCode, "response": proccess.result},
    )

    return proccess.result


@router.get(
    PathsEnum.mfa_code.value,
    response_model=MFASecretResponse,
    responses={
        200: {"model": MFASecretResponse, "description": "MFA secret is successfully"},
    },
    tags=["MFA"],
)
async def get_mfa_secret(
    response: Response,
    request: Request,
    get_mfa_secret_service: GetMFASecretService = Depends(get_mfa_secret_service),
    logger: CustomLogger = Depends(get_logger),
):
    logger.info(
        "Get MFA Secret",
        extra={"path": "POST /" + PathsEnum.mfa_code.value},
    )

    token = request.headers["authorization"]

    proccess = get_mfa_secret_service.execute(token)

    response.status_code = proccess.statusCode

    logger.info(
        "Proccess is finished",
        extra={"statusCode": proccess.statusCode, "response": proccess.result},
    )

    return proccess.result


@router.post(
    PathsEnum.mfa_challenge.value,
    response_model=ConfirmMFAResponse,
    responses={
        200: {"model": ConfirmMFAResponse, "description": "MFA secret is successfully"},
    },
    tags=["MFA"],
)
async def confirm_mfa(
    response: Response,
    payload: ConfirmMFARequest,
    confirm_mfa_service: ConfirmMFAService = Depends(confirm_mfa_service),
    logger: CustomLogger = Depends(get_logger),
):
    logger.info(
        "Get MFA Secret",
        extra={"path": "POST /" + PathsEnum.mfa_challenge.value},
    )

    proccess = confirm_mfa_service.execute(payload)

    response.status_code = proccess.statusCode

    logger.info(
        "Proccess is finished",
        extra={"statusCode": proccess.statusCode, "response": proccess.result},
    )

    return proccess.result
