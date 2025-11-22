resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Subnet
resource "aws_subnet" "main" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

# Route Table
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

# Security Group - VMs can communicate with each other
resource "aws_security_group" "main" {
  name   = "vm-communication"
  vpc_id = aws_vpc.main.id

  # SSH for Ubuntu
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # RDP for Windows
  ingress {
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = ["66.31.161.186/32"]
  }

  # Splunk Web Interface and doing attacks form your host
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["66.31.161.186/32"]
  }

  # Allow ALL traffic between VMs in the same subnet
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.1.0/24"]  # Allow all traffic from subnet
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Ubuntu VM - 8GB RAM, 100GB storage
resource "aws_instance" "ubuntu" {
  ami           = "ami-0e2c8caa4b6378d8c"
  instance_type = "t3.large"  # 8GB RAM
  subnet_id     = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.main.id]
  
  key_name = "soc"  # Add SSH key for access
  
  root_block_device {
    volume_size = 100  # 100GB storage
  }

  # ADD BASH COMMANDS HERE:
   user_data = base64encode(<<-EOF
    #!/bin/bash
    wget -O splunk-10.0.2-e2d18b4767e9-linux-amd64.deb "https://download.splunk.com/products/splunk/releases/10.0.2/linux/splunk-10.0.2-e2d18b4767e9-linux-amd64.deb"
    sudo dpkg -i splunk-10.0.2-e2d18b4767e9-linux-amd64.deb
    sudo -u splunk bash
    cd /opt/splunk/bin
   EOF
   )

  tags = {
    Name = "Ubuntu-VM"
  }
}

# Windows VM - 4GB RAM, 100GB storage
resource "aws_instance" "windows" {
  ami           = "ami-0159172a5a821bafd"
  instance_type = "t3.medium"  # 4GB RAM
  subnet_id     = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.main.id]
  
  key_name = "soc"
  # get_password_data = true

  # Allow all traffic from your IP and Ubuntu VM
  user_data = base64encode(<<-EOF
    <powershell>
    # Allow all traffic from your IP
    New-NetFirewallRule -DisplayName "Allow All from My IP" -Direction Inbound -RemoteAddress 66.31.161.186 -Action Allow
    New-NetFirewallRule -DisplayName "Allow All to My IP" -Direction Outbound -RemoteAddress 66.31.161.186 -Action Allow
    
    # Allow all traffic from Ubuntu subnet
    New-NetFirewallRule -DisplayName "Allow All from Subnet" -Direction Inbound -RemoteAddress 10.0.1.0/24 -Action Allow
    New-NetFirewallRule -DisplayName "Allow All to Subnet" -Direction Outbound -RemoteAddress 10.0.1.0/24 -Action Allow
    
    # Set network to Private profile
    Get-NetConnectionProfile | Set-NetConnectionProfile -NetworkCategory Private
    wget -O splunkforwarder-10.0.2-e2d18b4767e9-windows-x64.msi "https://download.splunk.com/products/universalforwarder/releases/10.0.2/windows/splunkforwarder-10.0.2-e2d18b4767e9-windows-x64.msi"
    </powershell>
  EOF
  )

  root_block_device {
    volume_size = 100  # 100GB storage
  }

  tags = {
    Name = "Windows-VM"
  }
}

# Outputs
output "ubuntu_ip" {
  value = aws_instance.ubuntu.public_ip
}

output "windows_ip" {
  value = aws_instance.windows.public_ip
}

output "ubuntu_private_ip" {
  value = aws_instance.ubuntu.private_ip
}

output "windows_private_ip" {
  value = aws_instance.windows.private_ip
}