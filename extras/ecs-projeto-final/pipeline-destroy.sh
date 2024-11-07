set -e

cd post-deployment/

rm -rf .terraform
terraform init -backend-config=environment/backend.tfvars
terraform destroy --auto-approve -var-file=environment/terraform.tfvars

cd ../
cd deployment/

rm -rf .terraform
terraform init -backend-config=environment/sa-east-1/backend.tfvars
terraform destroy --auto-approve -var-file=environment/sa-east-1/terraform.tfvars


cd ../
cd deployment/

rm -rf .terraform
terraform init -backend-config=environment/us-east-1/backend.tfvars
terraform destroy --auto-approve -var-file=environment/us-east-1/terraform.tfvars

cd ../
cd pre-deployment/

rm -rf .terraform
terraform init -backend-config=environment/backend.tfvars
terraform destroy --auto-approve -var-file=environment/terraform.tfvars