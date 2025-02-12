from fastapi import FastAPI
from mangum import Mangum

from src.infrastructure.controllers.signin_controller import router
from src.infrastructure.controllers.signup_controller import signup_router

# Crear la aplicación FastAPI
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# Incluir los controladores
app.include_router(router=router)
app.include_router(router=signup_router)


# Integración con AWS Lambda
lambda_handler = Mangum(app)
