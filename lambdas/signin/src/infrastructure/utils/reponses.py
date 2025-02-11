import json

from src.domain.models.dev_response import DevResponse


class ResponsesHelper:
    @staticmethod
    def to_json(reponse: DevResponse) -> str:
        dump = json.dumps(reponse.__dict__)
        return json.loads(dump)
