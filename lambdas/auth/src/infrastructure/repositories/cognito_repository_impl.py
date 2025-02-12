from typing import Optional, Self
from botocore.exceptions import ClientError
from botocore.client import BaseClient, ClientError

from src.domain.models.sm_lambda_auth_cognito import (
    SmLambdaAuthCognito,
)
from src.domain.repositories.cognito_repository import ICognitoRepository
from src.domain.models.cognito import CognitoInitiateAuth, CognitoInitiateAuthMFA
from src.infrastructure.utils.logger import CustomLogger


class CognitoRepositoryImpl(ICognitoRepository):
    """
    This class is responsible for implementing the CognitoRepository interface.
    """

    def __init__(
        self,
        logger: CustomLogger,
        cognito_client: BaseClient,
        cognito_configs: SmLambdaAuthCognito,
    ):
        """
        Initialize CognitoRepository with a specific type.

        Args:
            logger: Logger object
            cognito_client: Boto3 cognito client
            cognito_configs: Configuration values for the Cognito client
        """
        self.logger = logger
        self.cognito_client = cognito_client
        self.cognito_configs = cognito_configs

    def signin_with_email(
        self, email: str, password: str
    ) -> Optional[CognitoInitiateAuth | CognitoInitiateAuthMFA]:
        """
        Sign in with email and password.

        Args:
            email: Email of the user
            password: Password of the user to sign in

        Returns:
            The access token if the user is successfully signed in, None otherwise
        """
        return self.cognito_client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password,
            },
            ClientId=self.cognito_configs.client_id,
        )

    def get_mfa_secret(self, access_token: str) -> Optional[str]:
        """
        Gets a token that can be used to associate an MFA application with the user.

        :param session: Session information returned from a previous call to initiate
                        authentication.
        :return: An MFA token that can be used to set up an MFA application.
        """
        try:
            response = self.cognito_client.associate_software_token(
                AccessToken=access_token
            )

        except ClientError as err:
            self.logger.error(
                "Couldn't get MFA secret. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:

            return response["SecretCode"]

    def verify_mfa(
        self: Self,
        mfa_code: str,
        access_token: Optional[str] = None,
        session: Optional[str] = None,
    ) -> Optional[bool]:
        """
        Verify MFA with email and MFA code.

        Args:
            access_token: Access token of the user (optional).
            session: Session token of the user (optional).
            mfa_code: MFA code of the user to verify MFA.

        Returns:
            True if MFA was successfully verified, False otherwise.
        """

        if not (access_token or session):
            raise ValueError("Either access_token or session must be provided")

        try:
            if access_token:
                response = self.cognito_client.verify_software_token(
                    AccessToken=access_token, UserCode=mfa_code
                )
            else:
                response = self.cognito_client.verify_software_token(
                    Session=session, UserCode=mfa_code
                )
        except ClientError as err:
            self.logger.error(
                "Couldn't verify MFA:",
                extra={
                    "code": err.response["Error"]["Code"],
                    "message": err.response["Error"]["Message"],
                },
            )

            return False
        except ValueError as err:
            self.logger.error("Couldn't verify MFA.", extra={"err": err})

            return False
        else:
            self.logger.info("MFA verified successfully.", extra={"res": response})

            return response

    def software_token_auth_challenge(
        self, username: str, session: str, authenticator_code: str
    ):
        return self.cognito_client.respond_to_auth_challenge(
            ClientId=self.cognito_configs.client_id,
            Session=session,
            ChallengeName="SOFTWARE_TOKEN_MFA",
            ChallengeResponses={
                "USERNAME": username,
                "SOFTWARE_TOKEN_MFA_CODE": authenticator_code,
            },
        )
