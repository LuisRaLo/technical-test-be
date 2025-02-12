from botocore.exceptions import ClientError
from fastapi import status

from src.domain.models.cognito import CognitoInitiateAuth
from src.domain.models.sign_in import SignInResponse, SignInResult, SignInVerifyRequest
from src.domain.enums.messages import MessagesEnum
from src.domain.repositories.cognito_repository import ICognitoRepository
from src.domain.models.dev_response import DevResponse
from src.infrastructure.utils.logger import CustomLogger


class VerifyMFATokenService:
    def __init__(
        self,
        logger: CustomLogger,
        cognito_repository: ICognitoRepository,
    ):
        self.logger = logger
        self.cognito_repository = cognito_repository

    def execute(self, payload: SignInVerifyRequest) -> DevResponse:
        """
        Handle user sign-in process using username and password.

        Args:
            event: SignInVerifyRequest

        Returns:
            A token if sign-in is successful, None otherwise.
        """
        final_response = SignInResponse(
            mensaje=MessagesEnum.OPERATION_UNSUCCESSFULL.value
        )

        try:
            self.logger.debug("SESSION TOKEN", extra={"session": payload.session})

            verify_mfa = self.cognito_repository.software_token_auth_challenge(
                username=payload.user,
                session=payload.session,
                authenticator_code=payload.authenticator_code,
            )

            final_response.mensaje = MessagesEnum.OPERATION_SUCCESSFULL.value
            final_response = self.__format_response(verify_mfa)

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

    def __format_response(self, signin_response: CognitoInitiateAuth) -> SignInResponse:
        response = SignInResponse(
            mensaje=MessagesEnum.OPERATION_UNSUCCESSFULL.value, resultado=None
        )

        self.logger.debug(signin_response)

        # Check for missing fields and handle accordingly
        auth_result = signin_response.get("AuthenticationResult", {})
        if not auth_result:
            self.logger.error("AuthenticationResult is missing")
            response.mensaje = "Authentication result missing"
            return response

        result = SignInResult(
            authentication_result=auth_result,
            retry_attempts=int(
                signin_response.get("ChallengeParameters", {}).get("RetryAttempts", 0)
            ),
        )
        response.resultado = result

        self.logger.debug(response)

        return response
