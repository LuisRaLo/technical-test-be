from dataclasses import dataclass


@dataclass
class SmLambdaAuthCognito:
    name: str
    authority: str
    client_id: str
    client_secret: str
    server_metadata_url: str
    client_kwargs: dict
    user_pool_id: str
