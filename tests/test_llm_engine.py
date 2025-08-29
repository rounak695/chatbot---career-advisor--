import pytest
from unittest.mock import patch, MagicMock

from core.llm_engine import LLMEngine
from utils.errors import LLMResponseError

# Mock the AI message response object that LangChain would return
class MockAIMessage:
    def __init__(self, content):
        self.content = content

# Use a patch to replace the actual ChatOpenAI class during tests
@patch('core.llm_engine.ChatOpenAI')
def test_llm_engine_initialization_success(mock_chat_openai):
    """
    Tests if the LLMEngine initializes correctly with a valid API key.
    """
    mock_chat_openai.return_value = MagicMock()
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
        engine = LLMEngine()
        assert engine.llm is not None
        mock_chat_openai.assert_called_once_with(
            model="gpt-4o", temperature=0.7, api_key='test_key'
        )

def test_llm_engine_initialization_no_key():
    """
    Tests if the LLMEngine raises a ValueError if the API key is missing.
    """
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(LLMResponseError, match="Failed to initialize LLMEngine"):
            LLMEngine()

@patch('core.llm_engine.ChatOpenAI')
def test_generate_response_success(mock_chat_openai):
    """
    Tests a successful response generation flow, ensuring the chain is invoked correctly.
    """
    # Setup the mock for the entire chain invocation
    mock_llm_instance = MagicMock()
    mock_llm_instance.invoke.return_value = MockAIMessage("This is a mock career advice.")
    
    # We need to mock the chain object inside the LLMEngine instance
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
        engine = LLMEngine()
        # Directly mock the chain attribute of the instance
        engine.chain = MagicMock()
        engine.chain.invoke.return_value = MockAIMessage("This is a mock career advice.")

        response = engine.generate_response("session_123", "Tell me about software engineering.")
        
        assert response == "This is a mock career advice."
        engine.chain.invoke.assert_called_once_with(
            {"input": "Tell me about software engineering."},
            config={"configurable": {"session_id": "session_123"}}
        )

@patch('core.llm_engine.ChatOpenAI')
def test_generate_response_api_failure(mock_chat_openai):
    """
    Tests if a custom LLMResponseError is raised when the API call fails.
    """
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
        engine = LLMEngine()
        engine.chain = MagicMock()
        engine.chain.invoke.side_effect = Exception("API connection timed out")

        with pytest.raises(LLMResponseError, match="Error generating response from LLM"):
            engine.generate_response("session_456", "A question that will fail.")