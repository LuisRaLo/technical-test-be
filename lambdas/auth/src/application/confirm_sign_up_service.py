from typing import Self
from fastapi import status
from botocore.exceptions import ClientError

from src.domain.enums.messages import MessagesEnum
from src.domain.models.dev_response import DevResponse
from src.domain.models.sign_up import ConfirmSignUpRequest, SignUpResponse
from src.domain.repositories.cognito_repository import ICognitoRepository
from src.infrastructure.utils.logger import CustomLogger


class ConfirmSignUpService:
    def __init__(
        self: Self,
        logger: CustomLogger,
        cognito_repository: ICognitoRepository,
    ):
        self.logger = logger
        self.cognito_repository = cognito_repository

    def execute(self: Self, payload: ConfirmSignUpRequest) -> DevResponse:
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
            try_signup = self.cognito_repository.confirm_user_sign_up(
                user=payload.user,
                confirmation_code=payload.confirmation_code,
            )
        except ClientError as err:
            self.logger.error("Error in sign up service", extra={"error": str(err)})

            if err.response["Error"]["Code"] == "UsernameExistsException":
                final_response.mensaje = MessagesEnum.OPERATION_UNSUCCESSFULL.value
                final_response.resultado = MessagesEnum.USERNAME_EXISTS.value

                return DevResponse(
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    result=final_response.__dict__,
                )

            elif err.response["Error"]["Code"] == "ExpiredCodeException":
                final_response.mensaje = MessagesEnum.OPERATION_SUCCESSFULL.value
                final_response.resultado = "El código de confirmación ha expirado. Se ha enviado un nuevo código a su correo electrónico."

                process = self.cognito_repository.resend_confirmation(
                    user=payload.user,
                )

                self.logger.info(
                    "Proccess >>>>>>>",
                    extra={"proccess": process},
                )

                if process:
                    return DevResponse(
                        statusCode=status.HTTP_200_OK,
                        result=final_response.__dict__,
                    )
        final_response.mensaje = MessagesEnum.OPERATION_SUCCESSFULL.value
        final_response.resultado = try_signup

        return DevResponse(
            statusCode=status.HTTP_200_OK,
            result=final_response.__dict__,
        )
