# Career Guidance Chatbot - Design Document

## Table of Contents
- [System Overview](#system-overview)
- [Architecture Design](#architecture-design)
- [Database Design](#database-design)
- [Component Specifications](#component-specifications)
- [Integration Points](#integration-points)
- [Security Considerations](#security-considerations)
- [Deployment Architecture](#deployment-architecture)

## System Overview

### Project Goals
The Career Guidance Chatbot is designed to provide personalized career advice and guidance to users through an interactive conversational interface. The system combines rule-based logic, AI-powered responses, and data persistence to deliver a comprehensive career counseling experience.

### Key Features
- Interactive chat interface with natural language processing
- Rule-based career recommendation engine
- LLM integration for advanced conversational AI
- Google Sheets backend for data storage and analytics
- Export functionality for conversation history
- Real-time response with contextual awareness

### Target Users
- Job seekers looking for career guidance
- Students planning their career paths  
- Professionals considering career transitions
- Career counselors using the tool for client support

## Architecture Design

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│ Chatbot Framework│────│ Google Sheets   │
│   (Person A/D)  │    │   (Person A)     │    │   (Person A)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │              ┌──────────────────┐              │
         │              │  Rule Engine     │              │
         └──────────────│   (Person B)     │──────────────┘
                        └──────────────────┘
                                 │
                        ┌──────────────────┐
                        │   LLM Engine     │
                        │   (Person C)     │
                        └──────────────────┘
```

### Component Breakdown

#### 1. **Frontend Layer (Streamlit UI)**
- **Responsibility**: User interface, chat display, input handling
- **Owner**: Person A (framework), Person D (UX enhancements)
- **Key Files**:
  - `app.py` - Main application entry point
  - Custom CSS for styling
  - Session state management

#### 2. **Core Logic Layer (Chatbot Framework)**
- **Responsibility**: Message routing, intent detection, conversation flow
- **Owner**: Person A
- **Key Files**:
  - `core/chatbot_framework.py` - Main orchestration logic
  - Intent detection and context management
  - Response generation coordination

#### 3. **Business Logic Layer**
- **Rule Engine** (Person B): Career recommendation logic
- **LLM Engine** (Person C): AI-powered responses and fallback
- **Integration points for both systems

#### 4. **Data Layer (Google Sheets)**
- **Responsibility**: Data persistence, analytics, export functionality
- **Owner**: Person A
- **Key Files**:
  - `utils/sheets_api.py` - Google Sheets integration
  - Data schema and storage logic

#### 5. **Utilities Layer**
- **Formatting** (`utils/formatter.py`) - Message formatting and display
- **Error Handling** - Centralized error management
- **Logging** - System monitoring and debugging

## Database Design

### Google Sheets Schema

#### Sheet 1: `chat_messages`
| Column | Type | Description |
|--------|------|-------------|
| session_id | String | Unique identifier for chat session |
| timestamp | DateTime | ISO format timestamp |
| role | String | 'user' or 'assistant' |
| content | Text | Message content |
| metadata | JSON | Additional context data |

#### Sheet 2: `chat_exports`
| Column | Type | Description |
|--------|------|-------------|
| export_id | String | Unique export identifier |
| session_id | String | Related session ID |
| export_timestamp | DateTime | When export was created |
| message_count | Integer | Number of messages exported |
| export_data | JSON | Complete export payload |

#### Sheet 3: `session_analytics`
| Column | Type | Description |
|--------|------|-------------|
| session_id | String | Session identifier |
| start_time | DateTime | Session start timestamp |
| end_time | DateTime | Session end timestamp |
| message_count | Integer | Total messages in session |
| unique_intents | Integer | Number of different intents detected |
| topics | JSON Array | List of topics discussed |
| summary | JSON | Session summary data |

#### Sheet 4: `careers` (Person B)
| Column | Type | Description |
|--------|------|-------------|
| career_id | String | Unique career identifier |
| title | String | Career title |
| category | String | Career category/field |
| required_skills | JSON Array | List of required skills |
| education_level | String | Education requirements |
| salary_range | String | Typical salary range |
| growth_outlook | String | Job growth prospects |
| description | Text | Career description |

### Data Flow

1. **User Input** → Streamlit UI captures message
2. **Processing** → Chatbot Framework detects intent and routes
3. **Storage** → Message stored in Google Sheets
4. **Response Generation** → Rule Engine or LLM generates response
5. **Display** → Response formatted and shown to user
6. **Analytics** → Session data aggregated for insights

## Component Specifications

### ChatbotFramework Class

```python
class ChatbotFramework:
    def __init__(self):
        # Initialize intent patterns, response templates
        # Set up logging and conversation state tracking
        
    def detect_intent(self, message: str) -> str:
        # Pattern matching for intent classification
        # Returns: greeting, career_advice, skills_inquiry, etc.
        
    def get_context(self, session_id: str, history: List) -> Dict:
        # Build conversation context from message history
        # Extract mentioned topics, recent intents
        
    def process_message(self, message, session_id, history) -> str:
        # Main orchestration method
        # Coordinates intent detection, context building, response generation
        
    def generate_response(self, intent, context, message) -> str:
        # Generate appropriate response based on intent and context
        # Handles follow-up logic and contextual awareness
```

### SheetsAPI Class

```python
class SheetsAPI:
    def __init__(self):
        # Initialize Google Sheets client
        # Set up authentication and worksheet connections
        
    def append_message(self, message_data: Dict):
        # Store individual messages
        
    def save_chat_export(self, export_data: Dict):
        # Save complete conversation exports
        
    def get_session_messages(self, session_id: str) -> List:
        # Retrieve conversation history
        
    def save_session_analytics(self, analytics_data: Dict):
        # Store session analytics and summaries
```

## Integration Points

### Person A ↔ Person B Integration
- **Interface**: Career recommendation requests from chatbot framework
- **Data Exchange**: User preferences, skill assessments → Career suggestions
- **Error Handling**: Fallback to generic advice if rule engine fails

### Person A ↔ Person C Integration  
- **Interface**: LLM requests for complex queries and fallback responses
- **Data Exchange**: User message, conversation context → AI-generated response
- **Error Handling**: Graceful degradation to template responses

### Person A ↔ Person D Integration
- **Shared Components**: 
  - `app.py` - Main UI structure (Person A) + UX enhancements (Person D)
  - Testing coordination for end-to-end flows
  - Export functionality integration

## Security Considerations

### Data Protection
- **PII Handling**: No storage of personally identifiable information
- **Input Sanitization**: All user inputs sanitized before processing
- **Authentication**: Google Sheets access via service account credentials

### API Security
- **Credentials Management**: 
  - Streamlit secrets for sensitive data
  - Environment variables for deployment
  - No hardcoded credentials in codebase
- **Rate Limiting**: Prevent abuse of external APIs
- **Error Messages**: No sensitive information leaked in error responses

### Data Privacy
- **Session Isolation**: Each session tracked independently
- **Data Retention**: Define retention policies for conversation data
- **Export Controls**: Users can export their own data only

## Deployment Architecture

### Streamlit Cloud Deployment

```
┌─────────────────────────────────────────────────────┐
│                Streamlit Cloud                       │
│  ┌─────────────────┐  ┌─────────────────────────┐   │
│  │   App Instance  │  │    Environment Vars     │   │
│  │   - app.py      │  │    - GOOGLE_SHEETS_ID   │   │
│  │   - /core       │  │    - Other configs      │   │
│  │   - /utils      │  │                         │   │
│  └─────────────────┘  └─────────────────────────┘   │
└─────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────┐
│              Google Sheets API                       │
│  ┌─────────────────┐  ┌─────────────────────────┐   │
│  │   Spreadsheet   │  │    Service Account      │   │
│  │   - Messages    │  │    - Credentials        │   │
│  │   - Analytics   │  │    - Permissions        │   │
│  │   - Exports     │  │                         │   │
│  └─────────────────┘  └─────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Configuration Management

#### Streamlit Secrets (`secrets.toml`)
```toml
[google_sheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "service-account@project.iam.gserviceaccount.com"
client_id = "client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
spreadsheet_id = "your-spreadsheet-id"
```

#### Environment Variables
- `GOOGLE_SHEETS_CREDENTIALS` - JSON string of service account
- `GOOGLE_SHEETS_ID` - Spreadsheet identifier
- `LOG_LEVEL` - Logging verbosity
- `DEBUG_MODE` - Enable/disable debug features

### Performance Considerations

#### Response Time Optimization
- **Caching**: Cache common responses and intent patterns
- **Lazy Loading**: Load heavy resources only when needed
- **Connection Pooling**: Reuse Google Sheets connections

#### Scalability Planning
- **Session Management**: Efficient in-memory session storage
- **Database Optimization**: Batch writes to Google Sheets
- **Resource Monitoring**: Track memory and CPU usage

### Monitoring and Analytics

#### System Health
- **Error Tracking**: Log and monitor system errors
- **Performance Metrics**: Response times, success rates
- **Usage Analytics**: Session counts, popular features

#### Business Metrics
- **User Engagement**: Message counts, session duration
- **Feature Usage**: Most common intents, export usage
- **Content Quality**: User satisfaction indicators

## Testing Strategy

### Unit Tests
- Individual component functionality
- Mock external dependencies
- Edge case handling

### Integration Tests  
- End-to-end conversation flows
- Google Sheets integration
- Error recovery scenarios

### Performance Tests
- Response time benchmarks
- Memory usage monitoring
- Concurrent user simulation

### User Acceptance Tests
- Real user conversation flows
- Usability testing
- Feedback collection and analysis

This design document serves as the foundation for the Career Guidance Chatbot implementation, providing clear specifications for all team members and ensuring consistent architecture across all components.
