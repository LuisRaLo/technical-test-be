import json
import dacite
from typing import TypeVar, Optional, Type
from botocore.exceptions import ClientError
from botocore.client import BaseClient

from src.domain.repositories.secrets_manager_repository import (
    ISecretsManagerRepository,
)


# Define el tipo genérico T
T = TypeVar("T")


class SecretsManagerRepositoryImpl(ISecretsManagerRepository):
    """
    Implementation of the SecretsManagerRepository interface.
    This class interacts with AWS Secrets Manager and fetches secrets,
    returning them as either a raw string, dictionary, or dataclass.
    """

    def __init__(self, sm_client: BaseClient, secret_type: Type[T]):
        """
        Initialize the SecretsManagerRepositoryImpl with a Boto3 client and secret type.

        Args:
            sm_client: Boto3 secrets manager client
            secret_type: Type of the secret (dataclass, primitive type, etc.)
        """
        self.sm_client = sm_client
        self.secret_type = secret_type

    def get_secret(self, secret_name: str, default: Optional[T] = None) -> Optional[T]:
        """
        Fetch a secret from AWS Secrets Manager and deserialize it into the desired type.

        Args:
            secret_name: The name of the secret to retrieve from Secrets Manager.
            default: A default value to return if the secret is not found or can't be parsed.

        Returns:
            The secret value as the specified type T, or default if not found.

        Raises:
            ClientError: If an error occurs while accessing Secrets Manager.
            json.JSONDecodeError: If the secret can't be parsed as JSON.
            dacite.DaciteError: If the secret can't be converted to the dataclass.
        """
        try:
            # Attempt to retrieve the secret from AWS Secrets Manager
            get_secret_value_response = self.sm_client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # If the secret is not found, return the default value
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                return default
            # Re-raise the exception for other client errors
            raise e

        secret_string = get_secret_value_response.get("SecretString", "")
        if not secret_string:
            raise ValueError(
                f"Secret {secret_name} does not contain valid string data."
            )

        return self._deserialize_secret(secret_string, secret_name)

    def _deserialize_secret(self, secret_string: str, secret_name: str) -> Optional[T]:
        """
        Deserialize the secret string into the desired type (e.g., str, dict, dataclass).

        Args:
            secret_string: The string representation of the secret.
            secret_name: The name of the secret, used for error logging.

        Returns:
            The deserialized secret value.

        Raises:
            JSONDecodeError: If the secret can't be parsed as JSON.
            ValueError: If the secret can't be converted into the specified dataclass.
        """
        try:
            secret_dict = json.loads(secret_string)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Secret {secret_name} could not be parsed as JSON: {e.msg}",
                e.doc,
                e.pos,
            ) from e

        if self.secret_type is str:
            return secret_string  # Type directly returned if the expected type is str

        if self.secret_type is dict:
            return secret_dict  # Type directly returned if the expected type is dict

        if hasattr(self.secret_type, "__dataclass_fields__"):
            # If the type is a dataclass, deserialize it using dacite
            try:
                return dacite.from_dict(
                    data_class=self.secret_type,
                    data=secret_dict,
                    config=dacite.Config(strict=True),
                )
            except dacite.DaciteError as e:
                raise ValueError(
                    f"Could not convert secret {secret_name} to {self.secret_type.__name__}: {e}"
                ) from e

        # If the type is not handled, assume it's a primitive type and return the dict
        return secret_dict  # Default case for unsupported types
