from fastapi import FastAPI
from mangum import Mangum
from src.infrastructure.controllers.auth_controller import router

# Crear la aplicación FastAPI
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# Incluir los controladores
app.include_router(router=router)

# Integración con AWS Lambda
lambda_handler = Mangum(app)
