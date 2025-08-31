class LLMResponseError(Exception):
    """Raised when there's an error generating a response from the LLM"""
    pass

class SheetsAPIError(Exception):
    """Raised when there's an error with Google Sheets API operations"""
    pass

class RuleEngineError(Exception):
    """Raised when there's an error in the rule engine"""
    pass

class ChatbotFrameworkError(Exception):
    """Raised when there's an error in the main chatbot framework"""
    pass