import re
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

class ChatbotFramework:
    """
    Main chatbot framework that handles conversation flow, intent detection,
    and routing to appropriate response systems.
    """
    
    def __init__(self):
        self.conversation_state = {}
        self.intents = self._load_intents()
        self.responses = self._load_responses()
        self.context_history = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _load_intents(self) -> Dict[str, List[str]]:
        """Load intent patterns for message classification"""
        return {
            'greeting': [
                r'\b(hi|hello|hey|greetings)\b',
                r'\b(good\s+(morning|afternoon|evening))\b',
                r'\b(how\s+are\s+you)\b'
            ],
            'career_advice': [
                r'\b(career|job|profession|work)\b.*\b(advice|guidance|help|suggestion)\b',
                r'\b(what\s+career|which\s+job|what\s+profession)\b',
                r'\b(career\s+path|career\s+change|job\s+change)\b'
            ],
            'skills_inquiry': [
                r'\b(skills?|abilities|competenc|talent)\b.*\b(develop|learn|improve|need)\b',
                r'\b(what\s+skills|which\s+skills)\b',
                r'\b(skill\s+gap|lacking\s+skills)\b'
            ],
            'resume_help': [
                r'\b(resume|cv|curriculum\s+vitae)\b',
                r'\b(write\s+resume|resume\s+help|resume\s+advice)\b',
                r'\b(job\s+application|application\s+help)\b'
            ],
            'market_trends': [
                r'\b(job\s+market|market\s+trends|industry\s+trends)\b',
                r'\b(hiring\s+trends|employment\s+outlook)\b',
                r'\b(future\s+of\s+work|job\s+prospects)\b'
            ],
            'education': [
                r'\b(education|degree|certification|course|training)\b',
                r'\b(university|college|school|learning)\b',
                r'\b(study|academic|qualification)\b'
            ],
            'salary_inquiry': [
                r'\b(salary|pay|compensation|wage|income)\b',
                r'\b(how\s+much|earning\s+potential|pay\s+scale)\b'
            ],
            'interview_help': [
                r'\b(interview|interviewing)\b',
                r'\b(interview\s+prep|interview\s+questions|interview\s+tips)\b'
            ],
            'farewell': [
                r'\b(bye|goodbye|farewell|see\s+you|thanks?)\b',
                r'\b(that\'s\s+all|thank\s+you|appreciate)\b'
            ]
        }
    
    def _load_responses(self) -> Dict[str, List[str]]:
        """Load response templates for different intents"""
        return {
            'greeting': [
                "Hello! I'm your career guidance assistant. How can I help you with your professional journey today?",
                "Hi there! I'm here to help with career advice, job searching, and professional development. What would you like to know?",
                "Welcome! I'm excited to help you explore career opportunities and provide guidance. What's on your mind?"
            ],
            'career_advice': [
                "I'd be happy to help with career advice! To give you the best guidance, could you tell me more about your background, interests, or current situation?",
                "Career guidance is my specialty! What specific aspect of your career would you like to explore - choosing a path, changing careers, or advancing in your current field?",
                "Let's work together on your career journey! What are your main interests, skills, or career concerns right now?"
            ],
            'skills_inquiry': [
                "Developing the right skills is crucial for career success! What field or role are you targeting? I can suggest relevant skills to focus on.",
                "Skill development is a great investment! Are you looking to enhance skills for your current role or preparing for a career transition?",
                "I can help identify key skills for your career goals. What industry or position interests you most?"
            ],
            'resume_help': [
                "I'd be glad to help with your resume! Are you writing a new resume, updating an existing one, or targeting a specific role?",
                "Resume writing is important for job success! What type of position are you applying for? This will help me give targeted advice.",
                "Let's make your resume stand out! What's your field and experience level? I can provide specific tips."
            ],
            'market_trends': [
                "Job market insights can really help with career planning! Which industry or field interests you? I can share relevant trends.",
                "Understanding market trends is smart career strategy! Are you looking at a specific sector or general employment outlook?",
                "Market knowledge gives you an edge! What area of the job market would you like to explore?"
            ],
            'education': [
                "Education and training are valuable career investments! What field are you interested in, and what's your current education background?",
                "I can help you navigate education options! Are you considering formal degrees, certifications, or skill-specific training?",
                "Educational planning is key to career success! What are your career goals and current learning needs?"
            ],
            'salary_inquiry': [
                "Salary information is important for career decisions! What role or field are you curious about? Location also affects compensation.",
                "I can help with salary insights! What position interests you, and in which geographic area?",
                "Compensation varies by many factors! Tell me about the role and location you're considering."
            ],
            'interview_help': [
                "Interview preparation is crucial! What type of interview are you preparing for, and what role?",
                "I can definitely help with interview skills! Are you looking for general tips or preparation for a specific position?",
                "Interview success comes with good preparation! What's the role and company you're interviewing with?"
            ],
            'default': [
                "I understand you're looking for career guidance. Could you provide more specific details about what you'd like help with?",
                "I'm here to help with your career questions! Could you elaborate on what specific aspect you'd like to explore?",
                "I want to give you the most helpful advice. Could you tell me more about your career situation or goals?"
            ],
            'farewell': [
                "You're welcome! Best of luck with your career journey. Feel free to come back anytime for more guidance!",
                "I'm glad I could help! Remember, career development is a continuous process. Don't hesitate to reach out again!",
                "Thank you for using the career guidance chatbot! Wishing you success in your professional endeavors!"
            ]
        }
    
    def detect_intent(self, message: str) -> str:
        """Detect the intent of a user message"""
        message_lower = message.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return 'default'
    
    def get_context(self, session_id: str, message_history: List[Dict]) -> Dict[str, Any]:
        """Build context from conversation history"""
        context = {
            'session_id': session_id,
            'message_count': len(message_history),
            'recent_intents': [],
            'mentioned_topics': set(),
            'user_info': {}
        }
        
        # Analyze recent messages for context
        recent_messages = message_history[-5:] if len(message_history) > 5 else message_history
        
        for msg in recent_messages:
            if msg['role'] == 'user':
                intent = self.detect_intent(msg['content'])
                context['recent_intents'].append(intent)
                
                # Extract mentioned topics/keywords
                keywords = self._extract_keywords(msg['content'])
                context['mentioned_topics'].update(keywords)
        
        return context
    
    def _extract_keywords(self, text: str) -> set:
        """Extract relevant keywords from text"""
        # Common career-related keywords
        career_keywords = {
            'technology', 'software', 'programming', 'development', 'coding',
            'marketing', 'sales', 'finance', 'accounting', 'management',
            'healthcare', 'nursing', 'doctor', 'medical', 'engineering',
            'design', 'creative', 'writing', 'education', 'teaching',
            'consulting', 'business', 'startup', 'entrepreneur', 'leadership',
            'data', 'analytics', 'science', 'research', 'psychology',
            'law', 'legal', 'government', 'nonprofit', 'social work'
        }
        
        text_lower = text.lower()
        found_keywords = set()
        
        for keyword in career_keywords:
            if keyword in text_lower:
                found_keywords.add(keyword)
        
        return found_keywords
    
    def generate_response(self, intent: str, context: Dict[str, Any], message: str) -> str:
        """Generate appropriate response based on intent and context"""
        
        # Handle greeting with context awareness
        if intent == 'greeting':
            if context['message_count'] > 1:
                return "Hello again! How else can I assist you with your career questions?"
            else:
                import random
                return random.choice(self.responses['greeting'])
        
        # Handle follow-up questions
        if context['message_count'] > 1 and intent in context['recent_intents']:
            return self._generate_followup_response(intent, context, message)
        
        # Generate contextual response
        response = self._get_base_response(intent)
        
        # Enhance response with context
        if context['mentioned_topics']:
            topics = list(context['mentioned_topics'])[:2]  # Limit to 2 most recent
            if topics:
                topic_str = ', '.join(topics)
                response += f" I noticed you mentioned {topic_str}. This can help me provide more targeted advice!"
        
        return response
    
    def _generate_followup_response(self, intent: str, context: Dict[str, Any], message: str) -> str:
        """Generate follow-up responses for continuing conversations"""
        followup_responses = {
            'career_advice': [
                "Let me provide more specific guidance based on what you've shared. What particular aspect would you like to dive deeper into?",
                "Building on our previous discussion, what other career concerns or questions do you have?",
                "I see you're continuing to explore career options. What additional information would be most helpful?"
            ],
            'skills_inquiry': [
                "Great! Let's explore more skills for your career development. Are there specific areas you'd like to strengthen?",
                "Continuing with skill development - what challenges are you facing in acquiring these skills?",
                "What timeline are you working with for developing these new skills?"
            ],
            'resume_help': [
                "Let's continue improving your resume. What specific section would you like to focus on next?",
                "Building on your resume questions, what type of roles are you primarily targeting?",
                "What other resume concerns can I help address for you?"
            ]
        }
        
        if intent in followup_responses:
            import random
            return random.choice(followup_responses[intent])
        else:
            return self._get_base_response(intent)
    
    def _get_base_response(self, intent: str) -> str:
        """Get base response for intent"""
        import random
        
        if intent in self.responses:
            return random.choice(self.responses[intent])
        else:
            return random.choice(self.responses['default'])
    
    def process_message(self, message: str, session_id: str, message_history: List[Dict]) -> str:
        """
        Main method to process incoming messages and generate responses
        """
        try:
            # Detect intent
            intent = self.detect_intent(message)
            
            # Get context
            context = self.get_context(session_id, message_history)
            
            # Log for debugging
            self.logger.info(f"Session: {session_id[:8]}, Intent: {intent}, Context: {context['message_count']} messages")
            
            # Generate response
            response = self.generate_response(intent, context, message)
            
            # Update conversation state
            if session_id not in self.conversation_state:
                self.conversation_state[session_id] = {
                    'start_time': datetime.now().isoformat(),
                    'intents': [],
                    'topics': set()
                }
            
            self.conversation_state[session_id]['intents'].append(intent)
            self.conversation_state[session_id]['topics'].update(context['mentioned_topics'])
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return "I apologize, but I encountered an error processing your request. Please try rephrasing your question."
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of session for analytics"""
        if session_id in self.conversation_state:
            state = self.conversation_state[session_id]
            return {
                'session_id': session_id,
                'start_time': state['start_time'],
                'total_intents': len(state['intents']),
                'unique_intents': len(set(state['intents'])),
                'topics_discussed': list(state['topics']),
                'most_common_intent': max(set(state['intents']), key=state['intents'].count) if state['intents'] else None
            }
        return {}
    
    def reset_session(self, session_id: str):
        """Reset session state"""
        if session_id in self.conversation_state:
            del self.conversation_state[session_id]
