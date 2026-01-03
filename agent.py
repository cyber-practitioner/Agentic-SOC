from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tooling import get_current_alerts, get_alert_details,get_available_automations,trigger_automation,trigger_automation_with_data
import json

# Simple AI model
llm = ChatOllama(model="gpt-oss:20b", temperature=0.2)

# Super simple agent
agent = create_agent(
    llm,
    system_prompt="""
    You are a simple SOC assistant.
    You have access to various tools only respond to what the user wants to know about current security alerts.
    Use the tools to get information about alerts or anything else the user asks for  when needed.
    When a user requests to ask for an automation for a given alerts query the alert details using the tools and query the automations description to explain your thought process to the user when selecting an automation.
    explain your thought process to the user when selecting an automation  
    Be helpful and brief. No complex analysis needed.
    """,
    tools=[get_current_alerts, get_alert_details, get_available_automations,trigger_automation,trigger_automation_with_data]
)

def simple_chat():
    """Super simple chat interface"""
    print("🚀 Simple SOC Assistant")
    print("Commands: 'show alerts' or 'summarize [ID]' or 'exit'")
    
    conversation = []
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break
        
        # Add to conversation
        conversation.append({"role": "user", "content": user_input})
        
        try:
            # Get AI response

            result = agent.invoke({"messages": [{"role": "user", "content": f"{user_input}"}]})
            
            # Print AI response
            if 'messages' in result:
                ai_msg = result['messages'][-1]
                if isinstance(ai_msg, AIMessage):
                    print(f"\n🤖 Assistant: {ai_msg.content}")
                    conversation.append(ai_msg)
                    
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_chat()