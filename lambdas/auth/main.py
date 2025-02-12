from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from src.infrastructure.controllers.signin_controller import router
from src.infrastructure.controllers.signup_controller import signup_router

# Crear la aplicación FastAPI
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los controladores
app.include_router(router=router)
app.include_router(router=signup_router)


# Integración con AWS Lambda
lambda_handler = Mangum(app)
