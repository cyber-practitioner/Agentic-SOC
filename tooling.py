from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
import json
import re
from tines import TinesAPI

load_dotenv()

tines = TinesAPI(
        tenant_domain=os.getenv('TENANT_DOMAIN'),
        user_token= os.getenv('TINES_API_KEY')  # Complete your token
    )

@tool(description="Show current alerts")
def get_current_alerts() -> str:
    """Get ALL current alerts from the system"""
    try:
        response = requests.get(f"{os.getenv('NGROK_SERVER')}/alerts")
        data = response.json()
        alerts = data.get('alerts', [])
        
        if not alerts:
            return "No alerts found"
        
        result = f"📊 ALL CURRENT ALERTS ({len(alerts)} total):\n"
        result += "=" * 50 + "\n"
        
        # Show ALL alerts, not just 5
        for i, alert in enumerate(alerts, 1):
            alert_id = alert.get('sid', alert.get('id', 'N/A'))
            title = alert.get('search_name', 'Unknown')
            siem_url = alert.get('results_link', 'N/A')
            timestamp = alert.get('timestamp', 'Unknown')
            
            result += f"{i}. ID: {alert_id}\n"
            result += f"   Title: {title}\n"
            result += f"   SIEM URL: {siem_url}\n"
            result += f"   Time: {timestamp}\n"
            result += "-" * 30 + "\n"
        
        return result
        
    except Exception as e:
        return f"Error getting alerts: {str(e)}"


@tool(description="Get alert details")
def get_alert_details(alert_sid: str) -> str:
    """Get details of a specific alert"""
    try:
        response = requests.get(f"{os.getenv('NGROK_SERVER')}/alerts")
        data = response.json()
        alerts = data.get('alerts', [])
        
        for alert in alerts:
            if alert.get('sid') == alert_sid:
                complete_alert = json.dumps(alert, indent=2)
                title = alert.get('search_name', 'Unknown')
                summary = alert.get('ai_summary', 'No pre-existing summary available')
                threat = alert.get('threat_level', 'Unknown')
               

                return f"Alert {alert_sid}: {title}\nThreat: {threat}\nSummary: {summary}\nComplete Alert: {complete_alert}"

        return f"Alert {alert_sid} not found"
        
    except:
        return "Error getting alert details"

@tool(description="Get available automations")
def get_available_automations() -> str:
    """List available automations from Tines"""
    try:
        
        response = tines.list_stories()
        stories = response.get('stories', [])
        if not stories:
            return "No automations found"

        result = f"🤖 AVAILABLE AUTOMATIONS ({len(stories)} total):\n"
        result += "=" * 50 + "\n"
        
        for i, story in enumerate(stories, 1):
            story_id = story.get('id', 'N/A')
            name = story.get('name', 'Unknown')
            description = story.get('description', 'No description')
            if "URL: " in description:
                webhook_url = description.split("URL: ")[1]
            else:
                webhook_url = "Not found"

            result += f"{i}. ID: {story_id}\n"
            result += f"   Name: {name}\n"
            result += f"   Description: {description}\n"
            result += f"   Webhook URL: {webhook_url}\n"
            result += "-" * 30 + "\n"
        
        return result
        
    except Exception as e:
        return f"Error getting automations: {str(e)}"

@tool(description="Run a story that does not need alert data to run an automation and gather its results")
def trigger_automation(story_id: str) -> str:
    """Trigger a specific automation by ID"""
    try:
        story =tines.get_story(story_id)
        if story is None:
            return f"Automation with ID {story_id} not found"
        
        description = story.get('description', 'No description')
        if "URL: " in description:
                webhook_url = description.split("URL: ")[1]
        else:
                webhook_url = "Not found"
        response = requests.post(webhook_url)
        response_from_webserver = requests.get(f"{os.getenv('NGROK_SERVER')}/automation-response")
        if response_from_webserver.json()['response'].get('data'):
            return f"✅ Automation '{webhook_url}' triggered successfully!. Here is what is returned {response_from_webserver.json()['response'].get('data')}"
        else:
            return f"❌ Failed to trigger automation '{webhook_url}': {response.get('error', 'Unknown error')}"
    except Exception as e:
        return f"Error triggering automation: {str(e)}"

@tool(description="Trigger a story that does need alert data to a webhook and gather its results")
def trigger_automation_with_data(story_id: str, alert_data: dict) -> str:
    """Trigger a specific automation by ID and check its description for what data it needs"""
    try:
        story = tines.get_story(story_id)
        if story is None:
            return f"Automation with ID {story_id} not found"
        
        description = story.get('description', 'No description')
        if "URL: " in description:
            webhook_url = description.split("URL: ")[1]
        else:
            webhook_url = "Not found"
            return "No webhook found for the alert please add that somewhere i can find it"


        response = requests.post(webhook_url,json=alert_data)
        response_from_webserver = requests.get(f"{os.getenv('NGROK_SERVER')}/automation-response")
        if response_from_webserver.json()['response'].get('data'):
            return f"✅ Automation '{webhook_url}' triggered successfully!. Here is what is returned {response_from_webserver.json()['response'].get('data')}"
        else:
            return f"❌ Failed to trigger automation '{webhook_url}': {response.get('error', 'Unknown error')}"

    except Exception as e:
        return f"Error triggering automation: {str(e)}"