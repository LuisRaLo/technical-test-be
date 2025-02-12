from typing import Self
from botocore.exceptions import ClientError
from fastapi import status

from src.domain.models.mfa_secret import MFASecret, MFASecretResponse
from src.domain.enums.messages import MessagesEnum
from src.domain.repositories.cognito_repository import ICognitoRepository
from src.domain.models.dev_response import DevResponse
from src.infrastructure.utils.logger import CustomLogger


class GetMFASecretService:
    def __init__(
        self,
        logger: CustomLogger,
        cognito_repository: ICognitoRepository,
    ):
        self.logger = logger
        self.cognito_repository = cognito_repository

    def execute(self: Self, access_token: str) -> DevResponse:
        """
        Handle user sign-in process using username and password.

        Args:
            event: SignInVerifyRequest

        Returns:
            A token if sign-in is successful, None otherwise.
        """
        final_response = MFASecretResponse(
            mensaje=MessagesEnum.OPERATION_UNSUCCESSFULL.value
        )

        try:
            if not access_token:
                final_response.mensaje = MessagesEnum.UNAUTHORIZED.value

                return DevResponse(
                    statusCode=status.HTTP_401_UNAUTHORIZED,
                    result=final_response.__dict__,
                )

            bearer_token = access_token.split("Bearer ")[1]

            get_mfa_secret = self.cognito_repository.get_mfa_secret(bearer_token)

            final_response.mensaje = MessagesEnum.OPERATION_SUCCESSFULL.value
            final_response.resultado = MFASecret(secret=get_mfa_secret).__dict__

            return DevResponse(
                statusCode=status.HTTP_200_OK,
                result=final_response.__dict__,
            )

        except ClientError as err:
            self.logger.error("error", extra={"error": err})

            if err.response["Error"]["Code"] == "CodeMismatchException":
                final_response.mensaje = MessagesEnum.CODE_INVALID.value

                return DevResponse(
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    result=final_response.__dict__,
                )

            elif err.response["Error"]["Code"] == "InvalidParameterException":
                final_response.mensaje = MessagesEnum.PAYLOAD_ERROR.value

                return DevResponse(
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    result=final_response.__dict__,
                )

            elif err.response["Error"]["Code"] == "NotAuthorizedException":
                final_response.mensaje = MessagesEnum.SESSION_INVALID_OR_EXPIRED.value

                return DevResponse(
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    result=final_response.__dict__,
                )

            final_response.mensaje = MessagesEnum.INTERNAL_SERVER_ERROR.value

            return DevResponse(
                statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                result=final_response.__dict__,
            )
