#!/bin/bash

# Construir la función Lambda con contenedor
sam build LambdaSignInFunction --use-container

# Ejecutar el API Gateway localmente con las variables de entorno de locals.json
sam local start-api --env-vars lambdas/auth/locals.json --debug

# (Opcional) Invocar la función Lambda localmente con un archivo de evento
# sam local invoke LambdaSignInFunction --event lambdas/auth/mocks/signin.json \
#--env-vars lambdas/auth/locals.json \
#--debug
