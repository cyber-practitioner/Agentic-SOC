<powershell>
# Enable WinRM for remote management
Enable-PSRemoting -Force
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "*" -Force
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force

# Allow all traffic from your IP
New-NetFirewallRule -DisplayName "Allow All from My IP" -Direction Inbound -RemoteAddress 66.31.161.186 -Action Allow
New-NetFirewallRule -DisplayName "Allow All to My IP" -Direction Outbound -RemoteAddress 66.31.161.186 -Action Allow

# Allow all traffic from Ubuntu subnet
New-NetFirewallRule -DisplayName "Allow All from Subnet" -Direction Inbound -RemoteAddress 10.0.1.0/24 -Action Allow
New-NetFirewallRule -DisplayName "Allow All to Subnet" -Direction Outbound -RemoteAddress 10.0.1.0/24 -Action Allow

# Set network to Private profile
Get-NetConnectionProfile | Set-NetConnectionProfile -NetworkCategory Private

# Download Splunk Universal Forwarder to Downloads directory
wget -O C:\Users\Administrator\Downloads\splunkforwarder-10.0.2-e2d18b4767e9-windows-x64.msi "https://download.splunk.com/products/universalforwarder/releases/10.0.2/windows/splunkforwarder-10.0.2-e2d18b4767e9-windows-x64.msi"

# Install Splunk Universal Forwarder with parameters
#msiexec /i "C:\Users\Administrator\Downloads\splunkforwarder-10.0.2-e2d18b4767e9-windows-x64.msi" /quiet AGREETOLICENSE=yes SPLUNKPASSWORD=password RECEIVING_INDEXER="${ubuntu_private_ip}:9997"

# Log installation and configuration completion
Write-Output "Splunk Universal Forwarder installation and configuration completed" | Out-File -FilePath "C:\temp\splunk_install.log"
Write-Output "inputs.conf needs to be deployed successfully from template" | Out-File -FilePath "C:\temp\splunk_install.log" -Append
</powershell>