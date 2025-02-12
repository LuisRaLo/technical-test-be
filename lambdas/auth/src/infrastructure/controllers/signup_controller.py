from typing import Any
from fastapi import APIRouter, Depends, Response
from pydantic import ValidationError

from src.infrastructure.utils.exceptions import process_validation_error
from src.domain.models.sign_up import SignUpRequest
from src.infrastructure.utils.logger import CustomLogger

from src.domain.enums.paths_enum import PathsEnum
from src.application.sign_in_service import SignInService
from src.application.services import (
    get_logger,
    get_signin_service,
    get_verify_mfa_service,
)

signup_router = APIRouter()


@signup_router.post(
    PathsEnum.sign_up.value,
    response_model=Any,
    responses={
        200: {"model": Any, "description": "login is successfully"},
    },
)
async def signin(
    payload: SignUpRequest,
    response: Response,
    signin_service: SignInService = Depends(get_signin_service),
    logger: CustomLogger = Depends(get_logger),
):
    try:
        logger.info(
            "Init Proccess",
            extra={"path": PathsEnum.sign_up.value, "payload": payload},
        )

        return {"message": "Hello World"}
    except ValidationError as e:
        return process_validation_error(e)

    """ proccess = signin_service.sign_up(payload)  

        response.status_code = proccess.statusCode

        logger.info(
            "Proccess is finished",
            extra={"statusCode": proccess.statusCode, "response": proccess.result},
        )

        return proccess.result """
