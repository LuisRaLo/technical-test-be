from botocore.exceptions import ClientError
from fastapi import status

from src.domain.models.mfa_resend_code import ResendRequest
from src.domain.models.confirm_mfa import ConfirmMFARequest, ConfirmMFAResponse
from src.domain.enums.messages import MessagesEnum
from src.domain.repositories.cognito_repository import ICognitoRepository
from src.domain.models.dev_response import DevResponse
from src.infrastructure.utils.logger import CustomLogger


class ResendMFAService:
    def __init__(
        self,
        logger: CustomLogger,
        cognito_repository: ICognitoRepository,
    ):
        self.logger = logger
        self.cognito_repository = cognito_repository

    def execute(self, payload: ResendRequest) -> DevResponse:
        """
        Handle user sign-in process using username and password.

        Args:
            event: SignInVerifyRequest

        Returns:
            A token if sign-in is successful, None otherwise.
        """
        final_response = ConfirmMFAResponse(
            mensaje=MessagesEnum.OPERATION_UNSUCCESSFULL.value
        )

        try:
            verify_mfa = self.cognito_repository.resend_confirmation(user=payload.user)

            final_response.mensaje = MessagesEnum.OPERATION_SUCCESSFULL.value
            final_response.resultado = verify_mfa

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
