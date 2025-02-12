from typing import Any
from fastapi import APIRouter, Depends, Response
from pydantic import ValidationError

from src.infrastructure.utils.exceptions import process_validation_error
from src.infrastructure.utils.logger import CustomLogger
from src.domain.models.sign_up import (
    ConfirmSignUpRequest,
    SignUpRequest,
    SignUpResponse,
)
from src.domain.enums.paths_enum import PathsEnum
from src.application.services import (
    get_confirm_signup_service,
    get_logger,
    get_signup_service,
)
from src.application.sign_up_service import SignUpService

signup_router = APIRouter()


@signup_router.post(
    PathsEnum.sign_up.value,
    response_model=SignUpResponse,
    responses={
        200: {"model": SignUpResponse, "description": "login is successfully"},
    },
)
async def signup(
    payload: SignUpRequest,
    response: Response,
    signup_service: SignUpService = Depends(get_signup_service),
    logger: CustomLogger = Depends(get_logger),
):
    try:
        logger.info(
            "Init Proccess",
            extra={"path": PathsEnum.sign_up.value, "payload": payload},
        )

        proccess = signup_service.execute(payload)

        logger.info(
            "Proccess >>>>>>>",
            extra={"proccess": proccess},
        )

        response.status_code = proccess.statusCode

        logger.info(
            "Proccess is finished",
            extra={"statusCode": proccess.statusCode, "response": proccess.result},
        )

        return proccess.result
    except ValidationError as e:
        return process_validation_error(e)


@signup_router.post(
    PathsEnum.confirm_sign_up.value,
    response_model=Any,
    responses={
        200: {"model": Any, "description": "login is successfully"},
    },
)
async def confirm_sign_up(
    response: Response,
    payload: ConfirmSignUpRequest,
    confirm_signup_service=Depends(get_confirm_signup_service),
    logger: CustomLogger = Depends(get_logger),
):
    logger.info(
        "Init Proccess",
        extra={"path": PathsEnum.confirm_sign_up.value},
    )

    proccess = confirm_signup_service.execute(payload)

    logger.info(
        "Proccess >>>>>>>",
        extra={"proccess": proccess},
    )

    response.status_code = proccess.statusCode

    logger.info(
        "Proccess is finished",
        extra={"statusCode": proccess.statusCode, "response": proccess.result},
    )

    return proccess.result
