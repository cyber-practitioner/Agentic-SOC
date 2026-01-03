from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from langchain_core.messages import AIMessage
from datetime import datetime
import json

from pathlib import Path
import uvicorn

app = FastAPI(title="Splunk Webhook Receiver", version="1.0.0")
alerts_storage = []


@app.get('/dashboard', response_class=HTMLResponse)
def show_dashboard():
    return HTMLResponse(Path("frontend/dashboard.html").read_text())

@app.post('/splunk-webhook')
async def receive_splunk_alert(request: Request):
    """Receive and process Splunk alerts"""
    print(f"📨 Incoming alert received - Content-Type: {request.headers.get('content-type', 'unknown')}")
    
    alert_data = {}
    
    try:
        # Get the raw body first to check if it's empty
        body = await request.body()
        print(f"📨 Raw body length: {len(body)} bytes")
        
        if len(body) == 0:
            print("⚠️  Empty body received")
            alert_data = {"error": "Empty request body", "headers": dict(request.headers)}
        elif request.headers.get('content-type', '').startswith('application/json'):
            # Handle JSON content
            try:
                alert_data = json.loads(body.decode('utf-8'))
                print(f"📨 Received JSON alert: {alert_data}")
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON: {e}")
                alert_data = {"error": f"Invalid JSON: {str(e)}", "raw_body": body.decode('utf-8')}
        elif request.headers.get('content-type', '').startswith('multipart/form-data'):
            # Handle form data (current Tines format)
            form_data = await request.form()
            print(f"📨 Received form data keys: {list(form_data.keys())}")
            
            if form_data:
                webhook_json_str = list(form_data.keys())[0]
                print(f"📨 Form key (all chars): {webhook_json_str}...")
                try:
                   
                    alert_data = json.loads(webhook_json_str)
                    print(f"📨 Parsed webhook data: {alert_data.get('body')}")
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing webhook JSON: {e}")
                    alert_data = {"raw_form_key": webhook_json_str, "error": str(e)}
            else:
                alert_data = {"error": "Empty form data", "raw_body": body.decode('utf-8')}
        else:
            # Unknown content type - store as raw
            print(f"⚠️  Unknown content type: {request.headers.get('content-type')}")
            alert_data = {
                "raw_body": body.decode('utf-8'),
                "content_type": request.headers.get('content-type'),
                "headers": dict(request.headers)
            }
                
    except Exception as e:
        print(f"❌ Error processing request: {e}")
        alert_data = {"error": str(e), "headers": dict(request.headers)}
    
    # Add metadata
    alert_data['timestamp'] = datetime.now().isoformat()
    
    # STORE the alert (this is key!)
    alerts_storage.append(alert_data)
    
    # Keep only last 100 alerts to prevent memory issues
    if len(alerts_storage) > 100:
        alerts_storage.pop(0)
    
    # Here you could invoke the agent to process the alert
    
    
    return JSONResponse({"status": "received", "alert_id": alert_data['sid']})

@app.get('/alerts')
async def get_alerts():
    """Dashboard retrieves alerts from here"""

    # Return stored alerts (most recent first)
    recent_alerts = sorted(alerts_storage, key=lambda x: x['timestamp'], reverse=True)

    return JSONResponse({
        "alerts": recent_alerts,
        "total": len(alerts_storage)
    })

@app.get('/health')
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            'status': 'healthy', 
            'service': 'splunk-webhook-receiver'
        }
    )

# Simple storage - only one response at a time
current_response = None
is_response_pending = False

@app.post('/automation-response')
async def automation_response(request: Request):
    """Receive ONE automation response at a time"""
    global current_response, is_response_pending
    
    # Check if there's already a pending response
    if is_response_pending:
        return JSONResponse(
            status_code=429,  # Too Many Requests
            content={
                "error": "Cannot accept new request",
                "message": "Previous response not retrieved yet. Please GET first."
            }
        )
    
    # Accept new response
    data = await request.body()
    decoded_data = data.decode('utf-8')
    print(f"🤖 Automation response received: {decoded_data}")
    
    # Store the response and mark as pending
    current_response = {
        "data": decoded_data,
        "received_at": datetime.now().isoformat()
    }
    is_response_pending = True
    
    return JSONResponse({
        'status': 'response accepted',
        'message': 'Response stored. Retrieve with GET request.',
        'received_at': current_response['received_at']
    })

@app.get('/automation-response')
async def get_automation_response():
    """Get the current response and clear the queue"""
    global current_response, is_response_pending
    
    if not is_response_pending or current_response is None:
        return JSONResponse({
            "message": "No response available",
            "status": "empty"
        })
       # Return the response
    response_data = current_response
    
    # Clear the queue for next request
    current_response = None
    is_response_pending = False
    
    print("✅ Response retrieved and queue cleared")
    
    return JSONResponse({
        "response": response_data,
        "status": "retrieved"
    })

@app.get('/automation-status')
async def get_status():
    """Check if queue is free or busy"""
    return JSONResponse({
        "queue_status": "busy" if is_response_pending else "free",
        "has_pending_response": is_response_pending
    })
    
 

@app.get('/')
async def root():
    """Root endpoint with API info"""
    return JSONResponse(
        content={
            'message': 'Splunk Webhook Receiver API',
            'endpoints': {
                'webhook': '/splunk-webhook',
                'health': '/health',
                'docs': '/docs'
            }
        }
    )


#3ProCzgFHyHjc5tVoVF1

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)