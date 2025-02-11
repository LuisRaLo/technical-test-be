#!/usr/bin/env bash
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
WARNING='\033[0;33m'
NC='\033[0m'

ENV="${EnvStageName:=dev}"
REGION="${Region:=us-east-1}"
AWS_ACCOUNT_ID="${AWSAcctId:=730335368674}"
STACK_NAME="atenea-core-account-management-stack"

export GOPRIVATE=github.com/atene-ai/*
export CGO_ENABLED=0

MOCK_DIR="mocks"
LAMBDAS_DIR="handlers"

echo "⚙️) ${GREEN}Building Lambdas...${NC}"
for directory in $(find "$LAMBDAS_DIR" -type d -maxdepth 1 -mindepth 1); do
    dir_name=$(basename "$directory")
    echo "📁) ${GREEN}Checking ${NC}$dir_name ${GREEN}module...${NC}"
    if [ "$dir_name" != $MOCK_DIR ]; then
        echo "⚙️) ${GREEN}Building ${NC}$dir_name ${GREEN}module...${NC}"
        cd $LAMBDAS_DIR/"$dir_name" && env CGO_ENABLED=0 GOARCH=amd64 GOOS=linux GOAMD64=v1 go build -o bootstrap -ldflags="-s -w" && cd ../../
    fi
done


echo "Building Docker images"
sam build \
--use-container \
--parameter-overrides "ParameterKey=EnvStageName,ParameterValue=$ENV ParameterKey=Region,ParameterValue=$REGION"

echo "Deploying stack"
sam package \
--output-template-file packaged.yaml \
--s3-bucket "app-deploys-bucket" \
--image-repository "$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$STACK_NAME"

echo "Deploying stack"
sam deploy \
--template-file packaged.yaml \
--region $REGION \
--stack-name atenea-core-account-management-stack \
--s3-bucket "app-deploys-bucket" \
--capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
--image-repository "$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$STACK_NAME" \
--parameter-overrides "ParameterKey=EnvStageName,ParameterValue=$ENV ParameterKey=Region,ParameterValue=$REGION" \
--no-fail-on-empty-changeset \
--disable-rollback \
--tags project=atenea environment="${ENV}"