import streamlit as st
import json
from datetime import datetime
import uuid
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ... inside the user input section
if prompt:
    # ... code to display user message ...
    
    # Use the unique session ID from session_state
    response = framework.process_message(prompt, session_id=st.session_state.session_id)

from core.chatbot_framework import ChatbotFramework
from utils.sheets_api import SheetsAPI
from utils.formatter import format_message
import os

# Page configuration
st.set_page_config(
    page_title="Career Guidance Chatbot",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 2rem;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .timestamp {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .export-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatbotFramework()
    if 'sheets_api' not in st.session_state:
        try:
            st.session_state.sheets_api = SheetsAPI()
        except Exception as e:
            st.error(f"Failed to initialize Google Sheets connection: {e}")
            st.session_state.sheets_api = None

def save_message_to_sheets(role, content, metadata=None):
    """Save message to Google Sheets"""
    if st.session_state.sheets_api:
        try:
            message_data = {
                'session_id': st.session_state.session_id,
                'timestamp': datetime.now().isoformat(),
                'role': role,
                'content': content,
                'metadata': json.dumps(metadata) if metadata else ''
            }
            st.session_state.sheets_api.append_message(message_data)
        except Exception as e:
            st.error(f"Failed to save message: {e}")

def display_chat_history():
    """Display chat messages"""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", "")
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-header">👤 You</div>
                <div>{content}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-header">🤖 Career Bot</div>
                <div>{format_message(content)}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)

def export_chat_history():
    """Export chat history functionality"""
    if st.session_state.messages:
        # Create exportable format
        export_data = {
            'session_id': st.session_state.session_id,
            'export_timestamp': datetime.now().isoformat(),
            'messages': st.session_state.messages
        }
        
        # Convert to JSON string
        json_str = json.dumps(export_data, indent=2)
        
        # Create download button
        st.download_button(
            label="📥 Export Chat History (JSON)",
            data=json_str,
            file_name=f"chat_history_{st.session_state.session_id[:8]}.json",
            mime="application/json"
        )
        
        # Also save to sheets for history
        if st.session_state.sheets_api:
            try:
                st.session_state.sheets_api.save_chat_export(export_data)
                st.success("Chat history saved to Google Sheets!")
            except Exception as e:
                st.warning(f"Could not save to sheets: {e}")

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.title("🎯 Career Guidance Chatbot")
    st.markdown("Get personalized career advice and explore your professional path!")
    
    # Sidebar with session info and controls
    with st.sidebar:
        st.header("Session Info")
        st.write(f"**Session ID:** {st.session_state.session_id[:8]}...")
        st.write(f"**Messages:** {len(st.session_state.messages)}")
        
        if st.button("🔄 New Session"):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.chatbot = ChatbotFramework()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📤 Export")
        if st.session_state.messages:
            export_chat_history()
        else:
            st.info("Start a conversation to enable export")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display chat history
        chat_container = st.container()
        with chat_container:
            display_chat_history()
        
        # Chat input
        if prompt := st.chat_input("Ask me about career guidance..."):
            # Add user message to chat history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_message = {
                "role": "user",
                "content": prompt,
                "timestamp": timestamp
            }
            st.session_state.messages.append(user_message)
            
            # Save user message to sheets
            save_message_to_sheets("user", prompt)
            
            # Get bot response
            try:
                with st.spinner("Thinking..."):
                    ai_reply = st.session_state.chatbot.process_message(
                        prompt,
                        st.session_state.session_id
                    )
                
                # Add bot response to chat history
                bot_message = {
                    "role": "assistant",
                    "content": ai_reply,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.messages.append(bot_message)
                
                # Save bot message to sheets
                save_message_to_sheets("assistant", ai_reply)
                
            except Exception as e:
                st.error(f"Sorry, I encountered an error: {e}")
                error_message = {
                    "role": "assistant",
                    "content": "I apologize, but I'm experiencing technical difficulties. Please try again.",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.messages.append(error_message)
            
            # Rerun to display new messages
            st.rerun()
    
    with col2:
        # Quick actions and suggestions
        st.markdown("### 💡 Quick Actions")
        
        quick_prompts = [
            "What career suits my skills?",
            "How do I change careers?",
            "What skills should I develop?",
            "Tell me about job market trends",
            "Help me write a resume"
        ]
        
        for prompt in quick_prompts:
            if st.button(prompt, key=f"quick_{prompt}"):
                # Simulate clicking the prompt
                st.session_state.temp_prompt = prompt
                st.rerun()
        
        # Handle quick prompt selection
        if hasattr(st.session_state, 'temp_prompt'):
            prompt = st.session_state.temp_prompt
            del st.session_state.temp_prompt
            
            # Process the quick prompt same as manual input
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_message = {
                "role": "user", 
                "content": prompt,
                "timestamp": timestamp
            }
            st.session_state.messages.append(user_message)
            save_message_to_sheets("user", prompt)
            
            try:
                with st.spinner("Thinking..."):
                    ai_reply = st.session_state.chatbot.process_message(
                        prompt,
                        st.session_state.session_id
                    )
                
                bot_message = {
                    "role": "assistant",
                    "content": ai_reply,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.messages.append(bot_message)
                save_message_to_sheets("assistant", ai_reply)
                
            except Exception as e:
                st.error(f"Error: {e}")
            
            st.rerun()

if __name__ == "__main__":
    main()
