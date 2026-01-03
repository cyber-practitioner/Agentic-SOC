import boto3
import re
from botocore.exceptions import ClientError

def normalize_hostname(hostname):
    """
    Convert hostname formats like AR-WIN-1, AR-WIN-2 to ar-win for AWS searching
    """
    # Remove numbers and convert to lowercase
    normalized = re.sub(r'-?\d+$', '', hostname.lower())
    print(f"🔄 Converted hostname '{hostname}' to '{normalized}' for AWS search")
    return normalized

def block_rdp_access(attacker_ip, hostname):
    """
    Simplest function to block an IP from RDP access
    """
    print(f"🛡️ BLOCKING {attacker_ip} from RDP access to {hostname}")
    
    # Convert hostname format
    search_hostname = normalize_hostname(hostname)
    
    # Initialize EC2 client
    ec2 = boto3.client('ec2')
    
    try:
        # Find the Windows instance by normalized hostname
        response = ec2.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [f'*{search_hostname}*']},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        
        # Get security group from the instance
        security_group_id = None
        instance_name = None
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['SecurityGroups']:
                    security_group_id = instance['SecurityGroups'][0]['GroupId']
                    # Get the actual instance name
                    for tag in instance.get('Tags', []):
                        if tag['Key'] == 'Name':
                            instance_name = tag['Value']
                            break
                    break
        
        if not security_group_id:
            return f"❌ No security group found for hostname pattern '{search_hostname}'"
        
        print(f"🎯 Found instance: {instance_name}")
        print(f"🔒 Found security group: {security_group_id}")
        
        # Block the attacker IP from RDP port 3389
        try:
            ec2.revoke_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 3389,
                        'ToPort': 3389,
                        'IpRanges': [{'CidrIp': f'{attacker_ip}/32'}]
                    }
                ]
            )
            return f"✅ SUCCESS: Blocked {attacker_ip} from RDP access to {instance_name} (from alert: {hostname})"
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidPermission.NotFound':
                return f"ℹ️ {attacker_ip} was already blocked from RDP on {instance_name} - system is secure"
            else:
                return f"❌ Error: {e.response['Error']['Message']}"
                
    except Exception as e:
        return f"❌ Failed to block IP: {str(e)}"


# USAGE - Replace with your Splunk alert data
if __name__ == "__main__":
    # Test different hostname formats
    test_cases = [
        ("10.1.2.4", "AR-WIN-1")
    ]
    
    for attacker_ip, hostname in test_cases:
        print(f"\n{'='*60}")
        result = block_rdp_access(attacker_ip, hostname)
        print(result)