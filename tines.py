import requests
import json
from typing import Optional, Dict, Any, Union
import os
from dotenv import load_dotenv
load_dotenv()

class TinesAPI:
    def __init__(self, tenant_domain: str, user_token: str):
        self.tenant_domain = tenant_domain
        self.user_token = user_token
        self.base_url = f"https://{os.getenv('TENANT_DOMAIN')}/api/v1"

    def _make_request(self, method: str, endpoint: str,data: Optional[Union[Dict, str, bytes]] = None, **kwargs) -> Optional[Dict[Any, Any]]:
        """Make authenticated request to Tines API"""
       
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'x-user-token': self.user_token
        }
          # Handle different data types
        request_data = None
        if data is not None:
            if isinstance(data, dict):
                # Convert dict to JSON string
                request_data = json.dumps(data)
            elif isinstance(data, str):
                # Assume it's already JSON string
                request_data = data
            elif isinstance(data, bytes):
                # Use bytes directly
                request_data = data
                headers['Content-Type'] = 'application/octet-stream'
            else:
                # Try to convert to JSON
                try:
                    request_data = json.dumps(data)
                except (TypeError, ValueError):
                    print(f"Warning: Could not serialize data of type {type(data)}")
                    request_data = str(data)

        
        try:
            response = requests.request(method, url, headers=headers,data=request_data, **kwargs)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {response.status_code}: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
    
    def get_story(self, story_id: str) -> Optional[Dict[Any, Any]]:
        """Get a specific story by ID"""
        return self._make_request('GET', f'/stories/{story_id}')
    
    def list_stories(self) -> Optional[Dict[Any, Any]]:
        """List all stories"""
        return self._make_request('GET', '/stories')
    
    def run_a_story_using_webhook(self, webhook_url: str,data) -> Optional[Dict[Any, Any]]:
        """Trigger a story to run using a url and payload"""
        print(f"URL: {webhook_url}")
        print(f"Data: {data}")
        return self._make_request('POST', f'{webhook_url}',data)
    
    def get_agents(self, story_id: str) -> Optional[Dict[Any, Any]]:
        """Get agents for a specific story"""
        return self._make_request('GET', f'/stories/{story_id}/agents')

# Usage
if __name__ == "__main__":
    # Initialize Tines API client
    tines = TinesAPI(
        tenant_domain="dappled-bird-2161.tines.com",
        user_token= os.getenv('TINES_API_KEY')  # Complete your token
    )
    
    # Get the specific story
    story = tines.get_story("67400")
    print(story)
#    stories = tines.list_stories()
#    print(f"📊 Stories: {json.dumps(stories, indent=2)}")
'''
    story = None
    data ={'key':'value'}
    results = requests.post("https://dappled-bird-2161.tines.com/webhook/block-external-ip/c2e5749e303f3b030e04c9e5b35c8df4")
    response = requests.get(f"{os.getenv('NGROK_SERVER')}/automation-response")
    print(f"📊 Response Status Code: {response.status_code}")
    print(f"📊 Response Headers: {response.headers}")
    print(f"📊 Response Content: {response.text}")
    
    # Try to parse as JSON
    try:
        response_json = response.json()
        #print(f"📋 Parsed JSON Response: {json.dumps(response_json, indent=2)}")
        print(f"📄 Full Response body: {json.loads(response_json['response'].get('data')).get('body')}")
    except json.JSONDecodeError:
        print("❌ Response is not valid JSON")
    if story:
        print("✅ Story retrieved successfully!")
        print(f"Story Name: {story.get('name', 'N/A')}")
        print(f"Description: {story.get('description', 'N/A')}")
        print(f"Created: {story.get('created_at', 'N/A')}")
        print("\n📄 Full Story Data:")
        print(json.dumps(story, indent=2))
    else:
        print("❌ Failed to retrieve story")
    sotries = tines.list_stories()
    if sotries:
        print("✅ Stories listed successfully!")
        print("\n📄 Full Stories Data:")
        print(json.dumps(sotries, indent=2))
        '''