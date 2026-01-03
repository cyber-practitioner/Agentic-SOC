import requests,os,json
from dotenv import load_dotenv
load_dotenv()

# Just send a POST request
webhook_url = "https://dappled-bird-2161.tines.com/webhook/test/620c3c4701ee0f4729b1325f64da7102"
data_1 = {
    "sid": "scheduler__admin__search__T1078_at_1764357240_495",
    "search_name": "T1078",
    "app": "search",
    "owner": "admin",
    "results_link": "http://splunk-server:8000/app/search/@go?sid=scheduler__admin__search__T1078_at_1764357240_495",
    "result": {
        "timestamp": "2025-11-28 18:09:36 UTC",
        "computer": "ar-win-1",
        "event_id": "4672",
        "mitre_info": "T1078 - Valid Accounts",
        "attack_subtype": "T1078 - Valid Accounts (General)",
        "threat_level": "CRITICAL",
        "account_technique": "Special Privileges Assigned",
        "attack_pattern": "Debug Privileges Assigned (High Risk)",
        "final_target_user": "Unknown",
        "final_target_domain": "Unknown",
        "final_subject_user": "Administrator",
        "logon_type_desc": "Type Null",
        "source_ip": "10.1.2.4",
        "workstation": "",
        "final_process": "Unknown",
        "final_command": "Empty/Hidden",
        "risk_indicators": "Special privileges: SeSecurityPrivilege\n\t\t\tSeTakeOwnershipPrivilege\n\t\t\tSeLoadDriverPrivilege\n\t\t\tSeBackupPrivilege\n\t\t\tSeRestorePrivilege\n\t\t\tSeDebugPrivilege\n\t\t\tSeSystemEnvironmentPrivilege\n\t\t\tSeImpersonatePrivilege\n\t\t\tSeDelegateSessionUserImpersonatePrivilege",
        "detection_summary": "2025-11-28 18:09:36 UTC | ar-win-1 | CRITICAL | Debug Privileges Assigned (High Risk) | T1078 - Valid Accounts (General) | Special privileges: SeSecurityPrivilege\n\t\t\tSeTakeOwnershipPrivilege\n\t\t\tSeLoadDriverPrivilege\n\t\t\tSeBackupPrivilege\n\t\t\tSeRestorePrivilege\n\t\t\tSeDebugPrivilege\n\t\t\tSeSystemEnvironmentPrivilege\n\t\t\tSeImpersonatePrivilege\n\t\t\tSeDelegateSessionUserImpersonatePrivilege"
    }
}

data= {
    "sid": "scheduler__admin_U3BsdW5rX1NlY3VyaXR5X0Vzc2VudGlhbHM__RMD5284e8d034b502ff3_at_1766880240_1344",
    "search_name": "ai agent  powershell",
    "app": "Splunk_Security_Essentials",
    "owner": "admin",
    "results_link": "http://splunk-server:8000/app/Splunk_Security_Essentials/@go?sid=scheduler__admin_U3BsdW5rX1NlY3VyaXR5X0Vzc2VudGlhbHM__RMD5284e8d034b502ff3_at_1766880240_1344",
    "result": {
        "host": "EC2AMAZ-MQGI1B4",
        "event_count": "534",
        "interpreter_count": "3",
        "interpreters": [
            "cmd",
            "powershell",
            "rundll32"
        ],
        "processes": [
            "auditpol.exe",
            "bash.exe",
            "btool.exe",
            "chcp.com",
            "choco.exe",
            "cmd.exe",
            "conhost.exe",
            "csc.exe",
            "icacls.exe",
            "msiexec.exe",
            "net.exe",
            "powershell.exe",
            "reg.exe",
            "rundll32.exe",
            "scalar.exe",
            "setx.exe",
            "shutdown.exe",
            "splunk-powershell.exe",
            "splunk.exe",
            "sysmon64.exe"
        ],
        "parents": [
            "cmd.exe",
            "git-2.52.0-64-bit.tmp",
            "msiexec.exe",
            "powershell.exe",
            "splunk.exe",
            "splunkd.exe",
            "svchost.exe",
            "winrshost.exe"
        ],
        "process_paths": [
            "C:\\Program Files\\Git\\cmd\\scalar.exe",
            "C:\\Program Files\\Git\\usr\\bin\\bash.exe",
            "C:\\Program Files\\SplunkUniversalForwarder\\bin\\btool.exe",
            "C:\\Program Files\\SplunkUniversalForwarder\\bin\\splunk-powershell.exe",
            "C:\\Program Files\\SplunkUniversalForwarder\\bin\\splunk.exe",
            "C:\\Program Files\\ansible\\sysmon\\Sysmon64.exe",
            "C:\\ProgramData\\chocolatey\\bin\\choco.exe",
            "C:\\ProgramData\\chocolatey\\choco.exe",
            "C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\csc.exe",
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "C:\\Windows\\System32\\auditpol.exe",
            "C:\\Windows\\System32\\chcp.com",
            "C:\\Windows\\System32\\cmd.exe",
            "C:\\Windows\\System32\\conhost.exe",
            "C:\\Windows\\System32\\icacls.exe",
            "C:\\Windows\\System32\\msiexec.exe",
            "C:\\Windows\\System32\\net.exe",
            "C:\\Windows\\System32\\reg.exe",
            "C:\\Windows\\System32\\rundll32.exe",
            "C:\\Windows\\System32\\setx.exe",
            "C:\\Windows\\System32\\shutdown.exe"
        ],
        "parent_paths": [
            "C:\\Program Files\\SplunkUniversalForwarder\\bin\\splunk.exe",
            "C:\\Program Files\\SplunkUniversalForwarder\\bin\\splunkd.exe",
            "C:\\Users\\Administrator\\AppData\\Local\\Temp\\chocolatey\\is-B75ZF0T1VF.tmp\\Git-2.52.0-64-bit.tmp",
            "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "C:\\Windows\\System32\\cmd.exe",
            "C:\\Windows\\System32\\msiexec.exe",
            "C:\\Windows\\System32\\svchost.exe",
            "C:\\Windows\\System32\\winrshost.exe"
        ],
        "users": [
            "Administrator",
            "EC2AMAZ-MQGI1B4$"
        ],
        "process_ids": [
            "0x1008", "0x1020", "0x103c", "0x1040", "0x104c", "0x1064", "0x1074", "0x1078",
            "0x1108", "0x1124", "0x1134", "0x116c", "0x1174", "0x1188", "0x1194", "0x11b8",
            "0x11bc", "0x122c", "0x1234", "0x1254", "0x1264", "0x1278", "0x1298", "0x130",
            "0x1324", "0x1378", "0x1394", "0x13a4", "0x13c0", "0x140", "0x148", "0x150",
            "0x158", "0x178", "0x190", "0x194", "0x1cc", "0x1d4", "0x1dc", "0x218",
            "0x21c", "0x220", "0x234", "0x250", "0x264", "0x268", "0x288", "0x2a8",
            "0x2ac", "0x2b4", "0x2bc", "0x2d0", "0x2d4", "0x2d8", "0x2e0", "0x2f4",
            "0x2f8", "0x2fc", "0x308", "0x30c", "0x314", "0x328", "0x330", "0x338",
            "0x364", "0x368", "0x36c", "0x37c", "0x380", "0x384", "0x388", "0x3b0",
            "0x3b8", "0x3d8", "0x3dc", "0x408", "0x40c", "0x418", "0x420", "0x424",
            "0x430", "0x438", "0x440", "0x45c", "0x460", "0x48c", "0x494", "0x498",
            "0x4a4", "0x4a8", "0x4c8", "0x4d0", "0x4f0", "0x4f8", "0x530", "0x534",
            "0x538", "0x540", "0x55c", "0x560", "0x564", "0x56c", "0x578", "0x57c",
            "0x580", "0x58c", "0x590", "0x5a0", "0x5a8", "0x5b0", "0x5bc", "0x5cc",
            "0x5d4", "0x5e0", "0x5e4", "0x5e8", "0x5ec", "0x5f0", "0x62c", "0x63c",
            "0x644", "0x648", "0x650", "0x66c", "0x6ac", "0x6b0", "0x6bc", "0x6c4",
            "0x6c8", "0x6d0", "0x6d4", "0x6dc", "0x6f4", "0x6f8", "0x704", "0x708",
            "0x710", "0x71c", "0x724", "0x740", "0x744", "0x758", "0x760", "0x770",
            "0x778", "0x784", "0x788", "0x794", "0x798", "0x7a0", "0x7a4", "0x7bc",
            "0x7c0", "0x7d8", "0x7e8", "0x7f8", "0x808", "0x80c", "0x818", "0x81c",
            "0x824", "0x82c", "0x848", "0x850", "0x860", "0x868", "0x874", "0x890",
            "0x894", "0x898", "0x8a8", "0x8cc", "0x8e0", "0x900", "0x948", "0x94c",
            "0x954", "0x960", "0x964", "0x968", "0x97c", "0x984", "0x9a0", "0x9ac",
            "0x9b0", "0x9b4", "0x9b8", "0x9bc", "0x9c0", "0x9e0", "0xa04", "0xa0c",
            "0xa30", "0xa38", "0xa40", "0xa44", "0xa48", "0xa50", "0xa54", "0xa58",
            "0xa5c", "0xa64", "0xa68", "0xa84", "0xa8c", "0xa94", "0xaa8", "0xaac",
            "0xab8", "0xabc", "0xacc", "0xadc", "0xae0", "0xaf4", "0xb0c", "0xb14",
            "0xb1c", "0xb20", "0xb34", "0xb38", "0xb44", "0xb48", "0xb4c", "0xb54",
            "0xb58", "0xb94", "0xb9c", "0xbb0", "0xbb4", "0xbc0", "0xbcc", "0xbe4",
            "0xbe8", "0xbf4", "0xbf8", "0xbfc", "0xc14", "0xc18", "0xc24", "0xc28",
            "0xc3c", "0xc40", "0xc54", "0xc6c", "0xc70", "0xc7c", "0xc80", "0xc88",
            "0xc9c", "0xcc0", "0xccc", "0xcd4", "0xce0", "0xcec", "0xd3c", "0xd44",
            "0xd54", "0xd58", "0xd6c", "0xd84", "0xd8c", "0xda4", "0xda8", "0xdb8",
            "0xdc0", "0xde0", "0xe04", "0xe0c", "0xe10", "0xe14", "0xe18", "0xe1c",
            "0xe20", "0xe28", "0xe44", "0xe48", "0xe4c", "0xe54", "0xe58", "0xe64",
            "0xe6c", "0xe70", "0xe74", "0xe90", "0xe98", "0xea0", "0xeb0", "0xeb4",
            "0xebc", "0xec4", "0xed0", "0xed8", "0xedc", "0xee0", "0xef8", "0xf0c",
            "0xf10", "0xf14", "0xf20", "0xf24", "0xf2c", "0xf30", "0xf40", "0xf4c",
            "0xf50", "0xf54", "0xf58", "0xf60", "0xf68", "0xf6c", "0xf70", "0xf74",
            "0xf80", "0xf84", "0xf8c", "0xf9c", "0xfa0", "0xfa4", "0xfac", "0xfb0",
            "0xfb4", "0xfbc", "0xfc0", "0xfc4", "0xfc8", "0xfd0", "0xfd8", "0xfe8",
            "0xfec", "0xff0", "0xff8", "0xffc"
        ],
        "integrity_levels": [
            "Mandatory Label\\High Mandatory Level",
            "Mandatory Label\\System Mandatory Level"
        ],
        "first_seen": "12/27/2025 20:43:30",
        "last_seen": "12/27/2025 20:58:00",
        "execution_window_seconds": "870"
    }
}
webhook_url = 'https://dappled-bird-2161.tines.com/webhook/block-ip/6285d8d6fe0e67aa655624d14a23a380'
response = requests.post(webhook_url, json=data_1)
response_from_webserver = requests.get(f"{os.getenv('NGROK_SERVER')}/automation-response")
if response_from_webserver.json()['response'].get('data'):
    print(f"✅ Automation triggered successfully!. Here is what is returned {response_from_webserver.json()['response'].get('data')}")


#webhook_url_ngrok=" https://e0f023069d74.ngrok-free.app/splunk-webhook"
#response = requests.post(webhook_url_ngrok, json=data)
#response2 = requests.post(webhook_url_ngrok, json=data_1)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")