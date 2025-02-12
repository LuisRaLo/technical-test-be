from pydantic import ValidationError

from src.domain.models.dev_response import DevResponse


def process_validation_error(err: ValidationError) -> DevResponse:
    """
    Procesa una excepción ValidationError y la convierte en una instancia de DevResponse.
    """
    errors = []
    for error in err.errors():
        errors.append(
            {
                "field": ".".join(map(str, error["loc"])) if error["loc"] else "body",
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return DevResponse(
        statusCode=422,  # Código HTTP para "Unprocessable Entity"
        result={
            "status": "error",
            "message": "Validation failed",
            "errors": errors,
        },
    )
