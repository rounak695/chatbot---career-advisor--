import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from core.prompts import CAREER_ADVISOR_PROMPT
from utils.errors import LLMResponseError

class LLMEngine:
    def __init__(self):
        try:
            # Try to get the API key from Streamlit's secrets manager
            # Handle case where we're not in a Streamlit context
            try:
                if hasattr(st, 'secrets') and hasattr(st.secrets, 'openai'):
                    self.api_key = st.secrets.openai.api_key
                else:
                    # Fallback to environment variable or placeholder
                    import os
                    self.api_key = os.environ.get('OPENAI_API_KEY', 'placeholder-key')
            except Exception:
                # If we can't access Streamlit secrets, try environment variable
                import os
                self.api_key = os.environ.get('OPENAI_API_KEY', 'placeholder-key')
            
            if not self.api_key or self.api_key == 'placeholder-key':
                raise ValueError("OPENAI_API_KEY not found in Streamlit secrets or environment variables.")
            

            # Initialize the LLM model
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=self.api_key)

            # In-memory store for chat history.
            # In a real app, this might be a database or a more persistent store.
            self.chat_history_store = {}

            # Create the runnable chain with message history
            self.chain = RunnableWithMessageHistory(
                CAREER_ADVISOR_PROMPT | self.llm,
                self.get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
            )
        except Exception as e:
            raise LLMResponseError(f"Failed to initialize LLMEngine: {e}")

    def get_session_history(self, session_id: str):
        """
        Retrieves the chat history for a given session ID.
        If the session ID doesn't exist, it creates a new in-memory history.
        """
        if session_id not in self.chat_history_store:
            self.chat_history_store[session_id] = InMemoryChatMessageHistory()
        return self.chat_history_store[session_id]

    def generate_response(self, session_id: str, user_input: str) -> str:
        """
        Generates a response from the LLM for a given user input and session.

        Args:
            session_id: A unique identifier for the user's session.
            user_input: The user's message.

        Returns:
            The AI-generated response as a string.
        """
        if not user_input:
            return "Please provide some input."

        try:
            # Invoke the chain with the user input and session configuration
            response = self.chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
            return response.content
        except Exception as e:
            # Catch potential API errors and raise a custom exception
            raise LLMResponseError(f"Error generating response from LLM: {e}")