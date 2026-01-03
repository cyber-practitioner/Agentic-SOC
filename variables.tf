variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "availability_zone" {
  type        = string
  description = "AWS availability zone"
  default     = "us-east-1a"
}

variable "instance_name" {
  type        = string
  description = "EC2 instance name"
  default     = "agentic-soc-instance"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type - t3.large has 2 vCPUs and 8GB RAM"
  default     = "t3.large"  # 2 vCPUs, 8GB RAM - cost-effective option
}

variable "key_pair_name" {
  type        = string
  description = "Name of the AWS Key Pair for SSH access"
  default     = "agentic-soc-keypair"
}

variable "ssh_key_pub" {
  type        = string
  description = "Public SSH key contents for the EC2 instance (optional - will create key pair if provided)."
  default     = ""
}

variable "admin_cidr" {
  type        = string
  description = "CIDR allowed to SSH and access Wazuh (e.g. 66.31.161.186/32)."
  default     = "66.31.161.186/32"
}
