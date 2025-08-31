import json
from datetime import datetime
from typing import Dict, Any, List

def format_message(role: str, content: str, timestamp: str = None) -> Dict[str, Any]:
    """
    Format a chat message for display and storage.
    
    Args:
        role: The role of the message sender ('user' or 'assistant')
        content: The message content
        timestamp: Optional timestamp string
        
    Returns:
        Formatted message dictionary
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    return {
        "role": role,
        "content": content,
        "timestamp": timestamp
    }

def format_career_recommendation(career: Dict[str, Any]) -> str:
    """
    Format a career recommendation for display.
    
    Args:
        career: Career data dictionary
        
    Returns:
        Formatted career recommendation string
    """
    return f"""
**{career['title']}**
{career['description']}

**Salary Range**: ${career['salary_min']:,} - ${career['salary_max']:,}
**Experience Required**: {career['min_experience']} years
**Education**: {career['min_education'].title()}
**Growth Potential**: {career['growth_potential']}/10
**Market Demand**: {career['job_market_demand']}/10
"""

def format_export_data(messages: List[Dict[str, Any]], session_id: str) -> Dict[str, Any]:
    """
    Format chat data for export.
    
    Args:
        messages: List of chat messages
        session_id: Session identifier
        
    Returns:
        Formatted export data
    """
    return {
        "session_id": session_id,
        "export_timestamp": datetime.now().isoformat(),
        "total_messages": len(messages),
        "messages": messages
    }

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe file system operations.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    return sanitized
