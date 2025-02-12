from enum import Enum


class MessagesEnum(Enum):
    OPERATION_SUCCESSFULL = "Opeación realizada con éxito"
    OPERATION_UNSUCCESSFULL = "Opeación realizada sin éxito"
    PAYLOAD_ERROR = (
        "Verifica los valores que ingresaste sean correctos e intenta nuevamente"
    )
    CODE_INVALID = "Invalid code received for user"
    SESSION_INVALID_OR_EXPIRED = "Sesión no válida o expirada."
    INTERNAL_SERVER_ERROR = "Tenemos problemas con nuestro servicio, intente más tarde. Si persiste, favor de repostarlo."
    USERNAME_EXISTS = "El usuario ya existe."
    UNAUTHORIZED = "No autorizado."
