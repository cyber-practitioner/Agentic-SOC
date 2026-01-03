#!/bin/bash

echo "=========================================="
echo "AWS SOC Virtual Machines Deployment"
echo "=========================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "curl 'https://awscli.amazonaws.com/AWSCLIV2.pkg' -o 'AWSCLIV2.pkg'"
    echo "sudo installer -pkg AWSCLIV2.pkg -target /"
    exit 1
fi

# Check if Terraform is installed  
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install terraform
    else
        echo "Please install Terraform manually from: https://www.terraform.io/downloads.html"
        exit 1
    fi
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run:"
    echo "aws configure"
    exit 1
fi

echo "✅ Prerequisites met!"

# Choose deployment type
echo ""
echo "Choose deployment option:"
echo "1) Full Setup (Ubuntu 8GB + Windows 4GB) - ~$100/month"
echo "2) Free Tier (Ubuntu 1GB only) - FREE for 12 months"
echo "3) Cost Optimized (Spot instances) - ~$20/month"

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🚀 Deploying full setup..."
        terraform init
        terraform plan -out=tfplan
        terraform apply tfplan
        ;;
    2)
        echo "🆓 Deploying free tier setup..."
        cp free-tier-main.tf main-backup.tf
        mv main.tf main-full.tf
        mv free-tier-main.tf main.tf
        terraform init
        terraform plan -out=tfplan
        terraform apply tfplan
        ;;
    3)
        echo "💰 Deploying cost-optimized setup..."
        # Add spot instance configuration
        terraform init
        terraform plan -var="use_spot_instances=true" -out=tfplan
        terraform apply tfplan
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "🎉 Deployment Complete!"
echo "=========================================="

# Show connection info
terraform output

echo ""
echo "📋 Next Steps:"
echo "1. Connect to Ubuntu: ssh -i ~/.ssh/anshuma.pem ubuntu@[ubuntu_ip]"
echo "2. Connect to Windows: Use Remote Desktop to [windows_ip]"
echo "3. Default Windows password: SOCAgent123!"
echo "4. Install your SOC agent tools"
echo ""
echo "💡 Cost Management:"
echo "- Stop instances when not in use: aws ec2 stop-instances --instance-ids [id]"
echo "- Monitor costs in AWS Console"
echo "- Set up billing alerts"