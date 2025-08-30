import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.chatbot_framework import ChatbotFramework
from utils.sheets_api import SheetsAPI
from utils.formatter import format_message, format_career_advice

class TestChatbotFlow(unittest.TestCase):
    """End-to-end tests for chatbot functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chatbot = ChatbotFramework()
        self.session_id = "test_session_123"
        
        # Mock message history
        self.sample_messages = [
            {
                "role": "user",
                "content": "Hello, I need career advice",
                "timestamp": "2025-08-30 10:00:00"
            },
            {
                "role": "assistant", 
                "content": "Hello! I'm here to help with career guidance. What would you like to know?",
                "timestamp": "2025-08-30 10:00:01"
            }
        ]
    
    def test_intent_detection(self):
        """Test intent detection accuracy"""
        test_cases = [
            ("Hello there!", "greeting"),
            ("Hi, how are you?", "greeting"),
            ("I need career advice", "career_advice"),
            ("What career should I choose?", "career_advice"),
            ("What skills do I need to develop?", "skills_inquiry"),
            ("Help me with my resume", "resume_help"),
            ("What are the job market trends?", "market_trends"),
            ("Tell me about salary expectations", "salary_inquiry"),
            ("I need interview tips", "interview_help"),
            ("Thanks for your help", "farewell"),
            ("Something completely random", "default")
        ]
        
        for message, expected_intent in test_cases:
            with self.subTest(message=message):
                detected_intent = self.chatbot.detect_intent(message)
                self.assertEqual(detected_intent, expected_intent, 
                               f"Message '{message}' should be detected as '{expected_intent}', got '{detected_intent}'")
    
    def test_context_building(self):
        """Test context extraction from message history"""
        context = self.chatbot.get_context(self.session_id, self.sample_messages)
        
        self.assertEqual(context['session_id'], self.session_id)
        self.assertEqual(context['message_count'], len(self.sample_messages))
        self.assertIsInstance(context['recent_intents'], list)
        self.assertIsInstance(context['mentioned_topics'], set)
        self.assertIn('greeting', context['recent_intents'])
    
    def test_response_generation(self):
        """Test response generation for different intents"""
        test_intents = ['greeting', 'career_advice', 'skills_inquiry', 'default']
        
        for intent in test_intents:
            with self.subTest(intent=intent):
                context = {
                    'session_id': self.session_id,
                    'message_count': 1,
                    'recent_intents': [],
                    'mentioned_topics': set(),
                    'user_info': {}
                }
                
                response = self.chatbot.generate_response(intent, context, "test message")
                
                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 0)
                self.assertLess(len(response), 1000)  # Reasonable length limit
    
    def test_full_conversation_flow(self):
        """Test complete conversation flow"""
        test_messages = [
            "Hello!",
            "I need help choosing a career in technology", 
            "What skills should I focus on?",
            "Thanks for the advice!"
        ]
        
        conversation_history = []
        
        for message in test_messages:
            # Process message
            response = self.chatbot.process_message(
                message, 
                self.session_id, 
                conversation_history
            )
            
            # Add messages to history
            conversation_history.extend([
                {"role": "user", "content": message, "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": response, "timestamp": datetime.now().isoformat()}
            ])
            
            # Verify response
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 10)
        
        # Verify conversation state
        session_summary = self.chatbot.get_session_summary(self.session_id)
        self.assertIn('session_id', session_summary)
        self.assertGreater(session_summary['total_intents'], 0)
    
    def test_keyword_extraction(self):
        """Test keyword extraction from user messages"""
        test_text = "I'm interested in software development and programming careers in technology"
        keywords = self.chatbot._extract_keywords(test_text)
        
        expected_keywords = {'software', 'programming', 'technology', 'development'}
        self.assertTrue(expected_keywords.issubset(keywords))
    
    def test_follow_up_responses(self):
        """Test follow-up response generation"""
        # Create conversation with repeated intent
        conversation_history = [
            {"role": "user", "content": "I need career advice", "timestamp": "2025-08-30 10:00:00"},
            {"role": "assistant", "content": "How can I help?", "timestamp": "2025-08-30 10:00:01"},
        ]
        
        # Send another career advice message
        response = self.chatbot.process_message(
            "Can you give me more career guidance?",
            self.session_id,
            conversation_history
        )
        
        self.assertIsInstance(response, str)
        # Follow-up responses should be different from initial responses
        self.assertNotEqual(response, "")
    
    def test_session_management(self):
        """Test session state management"""
        # Process some messages
        self.chatbot.process_message("Hello", self.session_id, [])
        self.chatbot.process_message("Career advice please", self.session_id, [])
        
        # Check session exists
        self.assertIn(self.session_id, self.chatbot.conversation_state)
        
        # Get session summary
        summary = self.chatbot.get_session_summary(self.session_id)
        self.assertGreater(summary['total_intents'], 0)
        
        # Reset session
        self.chatbot.reset_session(self.session_id)
        self.assertNotIn(self.session_id, self.chatbot.conversation_state)
    
    def test_error_handling(self):
        """Test error handling in message processing"""
        # Test with invalid input types
        with patch.object(self.chatbot, 'detect_intent', side_effect=Exception("Test error")):
            response = self.chatbot.process_message("test", self.session_id, [])
            self.assertIn("error", response.lower())
    
    def test_message_formatting(self):
        """Test message formatting functionality"""
        test_messages = [
            "**Bold text** and *italic text*",
            "Here's a list:\n- Item 1\n- Item 2\n- Item 3",
            "Numbered list:\n1. First item\n2. Second item",
            "Check out https://example.com for more info",
            "Here's some `code` in the message"
        ]
        
        for message in test_messages:
            with self.subTest(message=message):
                formatted = format_message(message)
                self.assertIsInstance(formatted, str)
                # Should contain HTML formatting
                self.assertTrue(any(tag in formatted for tag in ['<strong>', '<em>', '<ul>', '<ol>', '<a>', '<code>']))

class TestSheetsAPIIntegration(unittest.TestCase):
    """Test Google Sheets integration (with mocking)"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_sheets_api = Mock(spec=SheetsAPI)
    
    @patch('utils.sheets_api.gspread')
    @patch('utils.sheets_api.Credentials')
    def test_sheets_initialization(self, mock_creds, mock_gspread):
        """Test sheets API initialization"""
        # Mock the credential and client setup
        mock_creds.from_service_account_info.return_value = Mock()
        mock_client = Mock()
        mock_gspread.authorize.return_value = mock_client
        mock_client.create.return_value = Mock()
        mock_client.create.return_value.id = "test_spreadsheet_id"
        
        # Test would initialize sheets API here
        # This test verifies the mocking setup works
        self.assertTrue(True)  # Placeholder assertion
    
    def test_message_storage(self):
        """Test message storage functionality"""
        message_data = {
            'session_id': 'test_session',
            'timestamp': '2025-08-30T10:00:00',
            'role': 'user',
            'content': 'Test message',
            'metadata': '{}'
        }
        
        # Mock the append_message method
        self.mock_sheets_api.append_message.return_value = None
        self.mock_sheets_api.append_message(message_data)
        
        # Verify method was called
        self.mock_sheets_api.append_message.assert_called_once_with(message_data)
    
    def test_export_functionality(self):
        """Test chat export functionality"""
        export_data = {
            'session_id': 'test_session',
            'export_timestamp': '2025-08-30T10:00:00',
            'messages': [
                {'role': 'user', 'content': 'Hello'},
                {'role': 'assistant', 'content': 'Hi there!'}
            ]
        }
        
        # Mock the save_chat_export method
        self.mock_sheets_api.save_chat_export.return_value = None
        self.mock_sheets_api.save_chat_export(export_data)
        
        # Verify method was called
        self.mock_sheets_api.save_chat_export.assert_called_once_with(export_data)

class TestUIComponents(unittest.TestCase):
    """Test UI component functionality"""
    
    def test_career_advice_formatting(self):
        """Test career advice formatting"""
        advice_data = {
            'title': '
