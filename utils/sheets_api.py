import os
import json
from typing import Dict, List, Any, Optional
import streamlit as st
from datetime import datetime
import logging

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

class SheetsAPI:
    """
    Google Sheets API helper class for storing and retrieving chat data
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.spreadsheet = None
        self.worksheets = {}
        
        if not GSPREAD_AVAILABLE:
            self.logger.warning("gspread not available. Running in offline mode.")
            return
            
        try:
            self._initialize_client()
            self._setup_worksheets()
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Sheets: {e}")
            raise
    
    def _initialize_client(self):
        """Initialize Google Sheets client"""
        # Try different credential sources
        creds = None
        
        # Method 1: Streamlit secrets
        if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
            try:
                # Load from streamlit secrets
                service_account_info = dict(st.secrets["google_sheets"])
                creds = Credentials.from_service_account_info(
                    service_account_info,
                    scopes=['https://spreadsheets.google.com/feeds',
                           'https://www.googleapis.com/auth/drive']
                )
                self.logger.info("Using Streamlit secrets for authentication")
            except Exception as e:
                self.logger.warning(f"Could not load from Streamlit secrets: {e}")
        
        # Method 2: Environment variable with JSON
        if not creds and 'GOOGLE_SHEETS_CREDENTIALS' in os.environ:
            try:
                creds_json = json.loads(os.environ['GOOGLE_SHEETS_CREDENTIALS'])
                creds = Credentials.from_service_account_info(
                    creds_json,
                    scopes=['https://spreadsheets.google.com/feeds',
                           'https://www.googleapis.com/auth/drive']
                )
                self.logger.info("Using environment variable for authentication")
            except Exception as e:
                self.logger.warning(f"Could not load from environment: {e}")
        
        # Method 3: Service account file
        if not creds and os.path.exists('.streamlit/secrets.toml'):
            try:
                # This is a fallback for local development
                creds = Credentials.from_service_account_file(
                    '.streamlit/service_account.json',
                    scopes=['https://spreadsheets.google.com/feeds',
                           'https://www.googleapis.com/auth/drive']
                )
                self.logger.info("Using service account file for authentication")
            except Exception as e:
                self.logger.warning(f"Could not load from service account file: {e}")
        
        if not creds:
            raise Exception("No valid Google Sheets credentials found")
        
        # Initialize client
        self.client = gspread.authorize(creds)
        
        # Get or create spreadsheet
        spreadsheet_id = self._get_spreadsheet_id()
        if spreadsheet_id:
            try:
                self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            except:
                # Create new spreadsheet if specified one doesn't exist
                self.spreadsheet = self.client.create("Career Bot Data")
                self.logger.info(f"Created new spreadsheet: {self.spreadsheet.id}")
        else:
            # Create new spreadsheet
            self.spreadsheet = self.client.create("Career Bot Data")
            self.logger.info(f"Created new spreadsheet: {self.spreadsheet.id}")
    
    def _get_spreadsheet_id(self) -> Optional[str]:
        """Get spreadsheet ID from various sources"""
        # Try Streamlit secrets first
        if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
            if 'spreadsheet_id' in st.secrets.google_sheets:
                return st.secrets.google_sheets.spreadsheet_id
        
        # Try environment variable
        return os.environ.get('GOOGLE_SHEETS_ID')
    
    def _setup_worksheets(self):
        """Setup required worksheets"""
        if not self.spreadsheet:
            return
            
        required_sheets = {
            'chat_messages': [
                'session_id', 'timestamp', 'role', 'content', 'metadata'
            ],
            'chat_exports': [
                'export_id', 'session_id', 'export_timestamp', 'message_count', 'export_data'
            ],
            'session_analytics': [
                'session_id', 'start_time', 'end_time', 'message_count', 
                'unique_intents', 'topics', 'summary'
            ]
        }
        
        for sheet_name, headers in required_sheets.items():
            try:
                # Try to get existing worksheet
                worksheet = self.spreadsheet.worksheet(sheet_name)
                self.worksheets[sheet_name] = worksheet
                
                # Check if headers exist, add if not
                existing_headers = worksheet.row_values(1)
                if not existing_headers or existing_headers != headers:
                    worksheet.update('A1', [headers])
                    self.logger.info(f"Updated headers for {sheet_name}")
                    
            except gspread.WorksheetNotFound:
                # Create new worksheet
                worksheet = self.spreadsheet.add_worksheet(
                    title=sheet_name, 
                    rows=1000, 
                    cols=len(headers)
                )
                worksheet.update('A1', [headers])
                self.worksheets[sheet_name] = worksheet
                self.logger.info(f"Created worksheet: {sheet_name}")
    
    def append_message(self, message_data: Dict[str, Any]):
        """Append a chat message to the messages worksheet"""
        if not self.client or 'chat_messages' not in self.worksheets:
            self.logger.warning("Cannot append message - sheets not initialized")
            return
        
        try:
            worksheet = self.worksheets['chat_messages']
            row_data = [
                message_data.get('session_id', ''),
                message_data.get('timestamp', ''),
                message_data.get('role', ''),
                message_data.get('content', ''),
                message_data.get('metadata', '')
            ]
            worksheet.append_row(row_data)
            self.logger.info(f"Appended message for session {message_data.get('session_id', '')[:8]}")
        except Exception as e:
            self.logger.error(f"Failed to append message: {e}")
            raise
    
    def save_chat_export(self, export_data: Dict[str, Any]):
        """Save chat export data"""
        if not self.client or 'chat_exports' not in self.worksheets:
            self.logger.warning("Cannot save export - sheets not initialized")
            return
        
        try:
            worksheet = self.worksheets['chat_exports']
            row_data = [
                export_data.get('session_id', ''),
                export_data.get('session_id', ''),
                export_data.get('export_timestamp', ''),
                len(export_data.get('messages', [])),
                json.dumps(export_data)
            ]
            worksheet.append_row(row_data)
            self.logger.info(f"Saved export for session {export_data.get('session_id', '')[:8]}")
        except Exception as e:
            self.logger.error(f"Failed to save export: {e}")
            raise
    
    def get_session_messages(self, session_id: str) -> List[Dict]:
        """Retrieve all messages for a session"""
        if not self.client or 'chat_messages' not in self.worksheets:
            return []
        
        try:
            worksheet = self.worksheets['chat_messages']
            records = worksheet.get_all_records()
            
            session_messages = []
            for record in records:
                if record['session_id'] == session_id:
                    session_messages.append({
                        'timestamp': record['timestamp'],
                        'role': record['role'],
                        'content': record['content'],
                        'metadata': json.loads(record['metadata']) if record['metadata'] else {}
                    })
            
            return sorted(session_messages, key=lambda x: x['timestamp'])
            
        except Exception as e:
            self.logger.error(f"Failed to get session messages: {e}")
            return []
    
    def save_session_analytics(self, session_data: Dict[str, Any]):
        """Save session analytics data"""
        if not self.client or 'session_analytics' not in self.worksheets:
            self.logger.warning("Cannot save analytics - sheets not initialized")
            return
        
        try:
            worksheet = self.worksheets['session_analytics']
            row_data = [
                session_data.get('session_id', ''),
                session_data.get('start_time', ''),
                session_data.get('end_time', datetime.now().isoformat()),
                session_data.get('message_count', 0),
                session_data.get('unique_intents', 0),
                json.dumps(session_data.get('topics', [])),
                json.dumps(session_data.get('summary', {}))
            ]
            worksheet.append_row(row_data)
            self.logger.info(f"Saved analytics for session {session_data.get('session_id', '')[:8]}")
        except Exception as e:
            self.logger.error(f"Failed to save analytics: {e}")
    
    def get_all_sessions(self) -> List[str]:
        """Get list of all session IDs"""
        if not self.client or 'chat_messages' not in self.worksheets:
            return []
        
        try:
            worksheet = self.worksheets['chat_messages']
            session_ids = worksheet.col_values(1)[1:]  # Skip header
            return list(set(session_ids))  # Remove duplicates
        except Exception as e:
            self.logger.error(f"Failed to get sessions: {e}")
            return []
    
    def get_recent_activity(self, days: int = 7) -> Dict[str, Any]:
        """Get recent activity summary"""
        if not self.client or 'chat_messages' not in self.worksheets:
            return {}
        
        try:
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days)
            worksheet = self.worksheets['chat_messages']
            records = worksheet.get_all_records()
            
            recent_records = []
            for record in records:
                try:
                    msg_time = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
                    if msg_time > cutoff_date:
                        recent_records.append(record)
                except:
                    continue
            
            # Analyze recent activity
            unique_sessions = len(set(r['session_id'] for r in recent_records))
            total_messages = len(recent_records)
            user_messages = len([r for r in recent_records if r['role'] == 'user'])
            
            return {
                'days_analyzed': days,
                'unique_sessions': unique_sessions,
                'total_messages': total_messages,
                'user_messages': user_messages,
                'bot_messages': total_messages - user_messages,
                'avg_messages_per_session': total_messages / max(unique_sessions, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get recent activity: {e}")
            return {}
    
    def health_check(self) -> Dict[str, Any]:
        """Check the health of the sheets connection"""
        health_status = {
            'gspread_available': GSPREAD_AVAILABLE,
            'client_initialized': self.client is not None,
            'spreadsheet_connected': self.spreadsheet is not None,
            'worksheets_setup': len(self.worksheets) > 0,
            'spreadsheet_id': self.spreadsheet.id if self.spreadsheet else None,
            'worksheet_count': len(self.worksheets)
        }
        
        # Test write capability
        try:
            if self.spreadsheet:
                # Try to access a worksheet
                test_sheet = list(self.worksheets.values())[0] if self.worksheets else None
                if test_sheet:
                    test_sheet.get('A1:A1')  # Simple read test
                    health_status['read_test'] = True
                else:
                    health_status['read_test'] = False
            else:
                health_status['read_test'] = False
        except Exception as e:
            health_status['read_test'] = False
            health_status['read_error'] = str(e)
        
        return health_status
