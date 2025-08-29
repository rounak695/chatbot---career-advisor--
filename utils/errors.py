class LLMResponseError(Exception):
    """
    Custom exception raised for errors related to the LLM engine.
    This can include API connection issues, authentication failures,
    or problems generating a response.
    """
    def __init__(self, message="An error occurred with the LLM service."):
        self.message = message
        super().__init__(self.message)