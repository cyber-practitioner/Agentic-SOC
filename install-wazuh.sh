#!/bin/bash
set -e

# Log file for debugging
LOG_FILE="/var/log/wazuh-install.log"
exec > >(tee -a $LOG_FILE)
exec 2>&1

echo "=== Wazuh Installation Script Started at $(date) ==="

# Update system packages
echo "Updating system packages..."
apt-get update -y
apt-get upgrade -y

# Install prerequisites
echo "Installing prerequisites..."
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    wget \
    unzip \
    software-properties-common \
    apt-transport-https

# Install Docker
echo "Installing Docker..."
# Add Docker's official GPG key
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index and install Docker
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker service
systemctl start docker
systemctl enable docker

# Add ubuntu user to docker group
usermod -aG docker ubuntu

# Verify Docker installation
echo "Verifying Docker installation..."
docker --version
docker compose version

# Set up Wazuh directory
WAZUH_DIR="/opt/wazuh-docker"
echo "Setting up Wazuh in $WAZUH_DIR..."

# Remove existing directory if it exists
if [ -d "$WAZUH_DIR" ]; then
    echo "Removing existing Wazuh directory..."
    rm -rf "$WAZUH_DIR"
fi

# Clone Wazuh Docker repository
echo "Cloning Wazuh Docker repository..."
cd /opt
git clone https://github.com/wazuh/wazuh-docker.git -b v4.13.1
cd "$WAZUH_DIR/single-node"

# Generate indexer certificates
echo "Generating Wazuh indexer certificates..."
docker compose -f generate-indexer-certs.yml run --rm generator

# Set proper ownership
chown -R ubuntu:ubuntu "$WAZUH_DIR"

# Create systemd service for Wazuh
echo "Creating Wazuh systemd service..."
cat > /etc/systemd/system/wazuh-stack.service << 'EOF'
[Unit]
Description=Wazuh Docker Stack
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/wazuh-docker/single-node
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0
User=ubuntu
Group=ubuntu

[Install]
WantedBy=multi-user.target
EOF

# Enable and start Wazuh service
systemctl daemon-reload
systemctl enable wazuh-stack.service

# Wait for Docker socket to be ready
echo "Waiting for Docker socket to be ready..."
sleep 10

# Start Wazuh stack
echo "Starting Wazuh stack..."
cd "$WAZUH_DIR/single-node"
sudo -u ubuntu docker compose up -d

# Wait for services to be ready
echo "Waiting for Wazuh services to start..."
sleep 60

# Check service status
echo "Checking Wazuh service status..."
sudo -u ubuntu docker compose ps

# Get container logs for verification
echo "Getting container status..."
sudo -u ubuntu docker compose logs --tail=20 wazuh.manager
sudo -u ubuntu docker compose logs --tail=20 wazuh.indexer
sudo -u ubuntu docker compose logs --tail=20 wazuh.dashboard

# Create health check script
echo "Creating health check script..."
cat > /opt/wazuh-health-check.sh << 'EOF'
#!/bin/bash
cd /opt/wazuh-docker/single-node
echo "=== Wazuh Stack Health Check ==="
echo "Container Status:"
docker compose ps
echo ""
echo "Wazuh Manager API Status:"
curl -k -u wazuh-wui:MyS3cr37P450r.*- https://localhost:55000/ 2>/dev/null || echo "API not ready yet"
echo ""
echo "Wazuh Dashboard Status:"
curl -k -I https://localhost:443 2>/dev/null | head -1 || echo "Dashboard not ready yet"
echo ""
echo "Services listening on ports:"
netstat -tlnp | grep -E ':(443|55000|9200|1514|1515)\s'
EOF

chmod +x /opt/wazuh-health-check.sh

# Install monitoring tools
echo "Installing monitoring tools..."
apt-get install -y htop iotop net-tools

# Configure firewall (ufw) - optional local firewall
echo "Configuring local firewall..."
ufw --force enable
ufw allow 22/tcp     # SSH
ufw allow 443/tcp    # Wazuh Dashboard
ufw allow 55000/tcp  # Wazuh API
ufw allow 1514/tcp   # Wazuh Agent
ufw allow 1515/tcp   # Wazuh Agent
ufw allow 514/udp    # Syslog
ufw reload

# Create useful aliases
echo "Creating useful aliases..."
cat >> /home/ubuntu/.bashrc << 'EOF'

# Wazuh aliases
alias wazuh-status='cd /opt/wazuh-docker/single-node && docker compose ps'
alias wazuh-logs='cd /opt/wazuh-docker/single-node && docker compose logs -f'
alias wazuh-stop='cd /opt/wazuh-docker/single-node && docker compose stop'
alias wazuh-start='cd /opt/wazuh-docker/single-node && docker compose start'
alias wazuh-restart='cd /opt/wazuh-docker/single-node && docker compose restart'
alias wazuh-health='/opt/wazuh-health-check.sh'
EOF

# Set proper permissions for home directory
chown -R ubuntu:ubuntu /home/ubuntu/

# Create completion indicator
echo "Installation completed at $(date)" > /var/log/wazuh-install-complete.txt

# Display final information
echo "=== Wazuh Installation Complete ==="
echo "Wazuh Dashboard: https://$(curl -s ifconfig.me):443"
echo "Default credentials: admin / SecretPassword"
echo "Wazuh API: https://$(curl -s ifconfig.me):55000"
echo "API credentials: wazuh-wui / MyS3cr37P450r.*-"
echo ""
echo "Useful commands:"
echo "  sudo /opt/wazuh-health-check.sh  # Check status"
echo "  wazuh-status                     # Container status"
echo "  wazuh-logs                       # View logs"
echo ""
echo "Log file: $LOG_FILE"
echo "=== Installation Script Finished at $(date) ==="