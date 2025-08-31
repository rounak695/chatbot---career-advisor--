# core/ux_enhancements.py
import json
from datetime import datetime
from typing import List, Dict, Any

def get_follow_up_suggestions(last_bot_message: str) -> List[str]:
    """
    Generate contextual follow-up questions based on the bot's last message.
    
    This is a simple placeholder. A more advanced version could use another
    LLM call or NLP to generate more relevant questions.
    """
    suggestions = [
        "Tell me more about the first option.",
        "What skills are needed for that?",
        "How does that compare to my current role?",
        "Can you explain that in simpler terms?"
    ]
    
    # Simple logic to avoid showing irrelevant follow-ups
    if "welcome" in last_bot_message.lower() or "hello" in last_bot_message.lower():
        return [
            "What career field are you interested in?",
            "Help me improve my resume.",
            "I want to change careers."
        ]
        
    return suggestions

def format_chat_history_for_export(messages: List[Dict[str, Any]]) -> str:
    """
    Formats the entire chat history into a human-readable string and then JSON.
    """
    
    # Create a human-readable header
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"CareerBot Conversation Export\nTimestamp: {timestamp}\n"
    
    # Format the conversation
    conversation_text = "\n\n".join(
        [f"{msg['role'].capitalize()}:\n{msg['content']}" for msg in messages]
    )
    
    export_data = {
        "export_timestamp_utc": datetime.utcnow().isoformat(),
        "total_messages": len(messages),
        "conversation": messages,
        "readable_transcript": f"{header}\n---\n\n{conversation_text}"
    }
    
    return json.dumps(export_data, indent=2)