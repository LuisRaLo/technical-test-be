from typing import Optional, Self
from fastapi import status

from botocore.exceptions import ClientError

from src.domain.models.sign_in import (
    SignInMFAResult,
    SignInRequest,
    SignInResponse,
    SignInResult,
)
from src.domain.repositories.cognito_repository import ICognitoRepository
from src.domain.models.cognito import CognitoInitiateAuth, CognitoInitiateAuthMFA
from src.domain.models.dev_response import DevResponse
from src.infrastructure.utils.logger import CustomLogger
from src.domain.enums.messages import MessagesEnum


class SignInService:
    def __init__(
        self: Self,
        logger: CustomLogger,
        cognito_repository: ICognitoRepository,
    ):
        self.logger = logger
        self.cognito_repository = cognito_repository

    def execute(self: Self, payload: SignInRequest) -> DevResponse:
        """
        Handle user sign-in process using username and password.

        Args:
            payload: SignInRequest

        Returns:
            A token if sign-in is successful, None otherwise.
        """
        final_response = SignInResponse(
            mensaje=MessagesEnum.OPERATION_UNSUCCESSFULL.value, resultado=None
        )

        try:
            try_sign_in = self.cognito_repository.signin_with_email(
                payload.user, payload.password
            )

            final_response = self.__format_response(try_sign_in)

            return DevResponse(
                statusCode=status.HTTP_200_OK, result=final_response.__dict__
            )

        except ClientError as e:
            self.logger.error(f"An error occurred: {e}")

            if e.response["Error"]["Code"] == "UserNotConfirmedException":
                final_response.mensaje = MessagesEnum.USER_NOT_CONFIRMED.value

            return DevResponse(
                statusCode=status.HTTP_404_NOT_FOUND,
                result=final_response.__dict__,
            )

        except Exception as err:
            self.logger.error(err)

            return DevResponse(
                statusCode=status.HTTP_409_CONFLICT, result=final_response.__dict__
            )

    def __format_response(
        self: Self,
        signin_response: Optional[CognitoInitiateAuth | CognitoInitiateAuthMFA],
    ) -> SignInResponse:
        response = SignInResponse(
            mensaje=MessagesEnum.OPERATION_UNSUCCESSFULL.value, resultado=None
        )

        self.logger.debug(signin_response)

        if signin_response.get("ChallengeName") is not None:
            result = SignInMFAResult(
                challenge_name=signin_response.get("ChallengeName"),
                session=signin_response.get("Session"),
                retry_attempts=int(
                    signin_response.get("ChallengeParameters", {}).get(
                        "RetryAttempts", 0
                    )
                ),
            )
            response.resultado = result
        else:
            result = SignInResult(
                challege_parameters=signin_response.get("ChallengeParameters"),
                authentication_result=signin_response.get("AuthenticationResult"),
                retry_attempts=int(
                    signin_response.get("ChallengeParameters", {}).get(
                        "RetryAttempts", 0
                    )
                ),
            )
            response.resultado = result

        self.logger.debug(response)

        return response
