#!/usr/bin/env bash
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
WARNING='\033[0;33m'
NC='\033[0m'

ENV="${EnvStageName:=dev}"
REGION="${Region:=us-east-1}"
AWS_ACCOUNT_ID="${AWSAcctId:=730335368674}"
STACK_NAME="creze-test-stack"


aws ecr describe-repositories --repository-names $STACK_NAME || aws ecr create-repository --repository-name $STACK_NAME


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
--stack-name  creze-test-stack \
--s3-bucket "app-deploys-bucket" \
--capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
--image-repository "$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$STACK_NAME" \
--parameter-overrides "ParameterKey=EnvStageName,ParameterValue=$ENV ParameterKey=Region,ParameterValue=$REGION" \
--no-fail-on-empty-changeset \
--disable-rollback \
--tags project=creze_test environment="${ENV}" owner=CrezeTest stackName="${STACK_NAME}" GitHubRepoName=technical-test-be
