#!/bin/bash

set -e

echo "INICIANDO ROLLOUT DO PRÉ-DEPLOYMENT"

cd pre-deployment/

rm -rf .terraform
terraform init -backend-config=environment/backend.tfvars
terraform apply --auto-approve -var-file=environment/terraform.tfvars


echo "FINALIZANDO ROLLOUT DO PRÉ-DEPLOYMENT"

cd ../

echo "INICIANDO ROLLOUT DA REGIAO US-EAST-1"

cd deployment/

rm -rf .terraform
terraform init -backend-config=environment/us-east-1/backend.tfvars
terraform apply --auto-approve -var-file=environment/us-east-1/terraform.tfvars


echo "FINALIZANDO ROLLOUT DA REGIAO US-EAST-1"

cd ../


echo "INICIANDO ROLLOUT DA REGIAO SA-EAST-1"

cd deployment/

rm -rf .terraform
terraform init -backend-config=environment/sa-east-1/backend.tfvars
terraform apply --auto-approve -var-file=environment/sa-east-1/terraform.tfvars


echo "FINALIZANDO ROLLOUT DA REGIAO SA-EAST-1"

cd ../

echo "INICIANDO ROLLOUT DO POST-DEPLOYMENT"

cd post-deployment/

rm -rf .terraform
terraform init -backend-config=environment/backend.tfvars
terraform apply --auto-approve -var-file=environment/terraform.tfvars

echo "FINALIZANDO ROLLOUT DO POST-DEPLOYMENT"

cd ../
