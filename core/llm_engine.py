import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

from core.prompts import CAREER_ADVISOR_PROMPT
from utils.errors import LLMResponseError

# Load environment variables from .env file
load_dotenv()

class LLMEngine:
    """
    Manages the connection and interaction with the OpenAI LLM via LangChain.
    """
    def __init__(self):
        """
        Initializes the LLM engine, chat history, and the conversation chain.
        """
        try:
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")

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