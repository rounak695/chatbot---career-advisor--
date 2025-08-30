from typing import Dict, Any
import logging
from datetime import datetime
from core.rule_engine import RuleEngine # Import Person B's work

class ChatbotFramework:
    def __init__(self):
        # ... existing __init__ code ...
        self.rule_engine = RuleEngine() # Initialize the RuleEngine
    
    def process_message(self, user_input: str, session_id: str) -> str:
        """
        Process user message and route to the appropriate engine.
        """
        # Simple keyword-based intent detection
        user_input_lower = user_input.lower()
        rule_based_keywords = ['find careers', 'recommend', 'suggest a job', 'based on my skills']

        # If a keyword is found, use the RuleEngine. Otherwise, use the LLM.
        if any(keyword in user_input_lower for keyword in rule_based_keywords):
            try:
                self.logger.info("Routing to RuleEngine.")
                return self.rule_engine.get_recommendations(user_input)
            except Exception as e:
                self.logger.error(f"Error in RuleEngine: {e}")
                return "I had an issue finding specific recommendations, but I can still help."

        # Fallback to LLMEngine for conversational queries
        try:
            if self.engine and LLM_AVAILABLE:
                self.logger.info("Routing to LLMEngine.")
                return self.engine.generate_response(session_id, user_input)
            else:
                return self._get_fallback_response(user_input)
        except Exception as e:
            self.logger.error(f"Error processing message with LLM: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."

# Import will be available when Person C creates the LLMEngine
try:
    from core.llm_engine import LLMEngine
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

class ChatbotFramework:
    """
    Simplified chatbot framework that integrates with LLMEngine.
    
    This class serves as a thin wrapper around the LLMEngine,
    providing any additional orchestration logic needed.
    """
    
    def __init__(self):
        """Initialize the chatbot framework"""
        self.logger = logging.getLogger(__name__)
        
        if LLM_AVAILABLE:
            # Create an instance of the LLMEngine class
            self.engine = LLMEngine()
            self.logger.info("LLMEngine initialized successfully")
        else:
            self.engine = None
            self.logger.warning("LLMEngine not available, using fallback responses")
        
        # Simple fallback responses when LLMEngine is not available
        self.fallback_responses = [
            "I'm here to help with your career questions! Could you tell me more about what you're looking for?",
            "I'd be happy to provide career guidance. What specific area would you like to explore?",
            "Let me assist you with your career journey. What's your main concern or goal right now?",
            "I'm ready to help with career advice! What would you like to know?",
        ]
    
    def process_message(self, user_input: str, session_id: str) -> str:
        """
        Process user message and return AI response.
        
        Args:
            user_input: The user's message
            session_id: Unique session identifier
            
        Returns:
            AI-generated response string
        """
        try:
            if self.engine and LLM_AVAILABLE:
                # Call one method to get a response
                ai_reply = self.engine.generate_response(session_id, user_input)
                return ai_reply
            else:
                # Fallback response when LLMEngine is not available
                return self._get_fallback_response(user_input)
                
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again."
    
    def _get_fallback_response(self, user_input: str) -> str:
        """
        Generate a fallback response when LLMEngine is not available.
        
        Args:
            user_input: The user's message
            
        Returns:
            Simple fallback response
        """
        import random
        
        # Basic keyword detection for simple responses
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm your career guidance assistant. How can I help you with your professional journey today?"
        
        elif any(word in user_input_lower for word in ['career', 'job', 'work', 'profession']):
            return "I'd be happy to help with career advice! To give you the best guidance, could you tell me more about your background, interests, or current situation?"
        
        elif any(word in user_input_lower for word in ['skills', 'abilities', 'learn', 'develop']):
            return "Developing the right skills is crucial for career success! What field or role are you targeting? I can suggest relevant skills to focus on."
        
        elif any(word in user_input_lower for word in ['resume', 'cv', 'application']):
            return "I'd be glad to help with your resume! Are you writing a new resume, updating an existing one, or targeting a specific role?"
        
        elif any(word in user_input_lower for word in ['salary', 'pay', 'money', 'compensation']):
            return "Salary information is important for career decisions! What role or field are you curious about? Location also affects compensation."
        
        elif any(word in user_input_lower for word in ['thanks', 'thank you', 'bye', 'goodbye']):
            return "You're welcome! Best of luck with your career journey. Feel free to come back anytime for more guidance!"
        
        else:
            return random.choice(self.fallback_responses)
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the chatbot framework.
        
        Returns:
            Health status dictionary
        """
        return {
            'framework_initialized': True,
            'llm_engine_available': LLM_AVAILABLE and self.engine is not None,
            'fallback_mode': not (LLM_AVAILABLE and self.engine is not None),
            'timestamp': datetime.now().isoformat()
        }
    
    def reset_session(self, session_id: str):
        """
        Reset session state if needed.
        
        Args:
            session_id: Session to reset
        """
        # The LLMEngine handles its own session management
        # This method is here for compatibility if needed
        self.logger.info(f"Session reset requested for {session_id}")
        pass
