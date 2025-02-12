from typing import Self
from fastapi import status

from src.domain.enums.messages import MessagesEnum
from src.domain.models.dev_response import DevResponse
from src.domain.models.sign_up import SignUpRequest, SignUpResponse
from src.domain.repositories.cognito_repository import ICognitoRepository
from src.infrastructure.utils.logger import CustomLogger


class SignUpService:
    def __init__(
        self: Self,
        logger: CustomLogger,
        cognito_repository: ICognitoRepository,
    ):
        self.logger = logger
        self.cognito_repository = cognito_repository

    def execute(self: Self, payload: SignUpRequest) -> DevResponse:
        """
        Execute the sign up service.

        Args:
            payload: The sign up request

        Returns:
            The response of the sign up service
        """
        final_response = SignUpResponse(
            mensaje=MessagesEnum.OPERATION_UNSUCCESSFULL.value
        )

        self.logger.info("Init Proccess", extra={"payload": payload})

        try:
            try_signup = self.cognito_repository.signup(
                email=payload.email,
                password=payload.password,
                name=payload.name,
            )
        except Exception as err:
            self.logger.error("Error in sign up service", extra={"error": str(err)})

            if err.response["Error"]["Code"] == "UsernameExistsException":
                final_response.mensaje = MessagesEnum.OPERATION_UNSUCCESSFULL.value
                final_response.resultado = MessagesEnum.USERNAME_EXISTS.value

                return DevResponse(
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    result=final_response.__dict__,
                )

        final_response.mensaje = MessagesEnum.OPERATION_SUCCESSFULL.value
        final_response.resultado = try_signup

        return DevResponse(
            statusCode=status.HTTP_200_OK,
            result=final_response.__dict__,
        )
