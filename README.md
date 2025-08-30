# Career Guidance Chatbot 🎯

An intelligent career counseling chatbot built with Streamlit that provides personalized career advice through conversational AI, rule-based recommendations, and comprehensive data analytics.

## 🌟 Features

- **Interactive Chat Interface**: Clean, responsive UI built with Streamlit
- **Multi-Engine Response System**: Combines rule-based logic with LLM integration
- **Google Sheets Backend**: Persistent storage and analytics
- **Conversation Export**: Download chat history for future reference
- **Real-time Analytics**: Track user interactions and conversation patterns
- **Intent Detection**: Smart routing based on user query types

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│ Chatbot Framework│────│ Google Sheets   │
│     Frontend    │    │   Orchestrator   │    │    Storage      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                    ┌─────────────────────────────┐
                    │                             │
            ┌──────────────┐            ┌──────────────┐
            │ Rule Engine  │            │  LLM Engine  │
            │   (Person B) │            │  (Person C)  │
            └──────────────┘            └──────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud account with Sheets API access
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd career-bot
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Google Sheets**
   - Create a Google Cloud project
   - Enable Google Sheets API
   - Create service account and download JSON credentials
   - Create a Google Sheets document for data storage

4. **Set up Streamlit secrets**
   ```bash
   mkdir .streamlit
   ```
   
   Create `.streamlit/secrets.toml`:
   ```toml
   [google_sheets]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_KEY\n-----END PRIVATE KEY-----\n"
   client_email = "your-service-account@your-project.iam.gserviceaccount.com"
   client_id = "your-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   spreadsheet_id = "your-spreadsheet-id"
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will be available at `http://localhost:8501`

## 📁 Project Structure

```
career-bot/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── .streamlit/                     # Streamlit configuration
│   ├── config.toml                 # App configuration
│   └── secrets.toml                # API credentials (not in git)
│
├── core/                           # Core business logic
│   ├── chatbot_framework.py        # Main orchestration (Person A)
│   ├── rule_engine.py              # Career rules (Person B)
│   ├── llm_engine.py               # AI integration (Person C)
│   ├── prompts.py                  # LLM prompts (Person C)
│   └── ux_enhancements.py          # UI improvements (Person D)
│
├── utils/                          # Utility modules
│   ├── formatter.py                # Message formatting
│   ├── errors.py                   # Error handling
│   └── sheets_api.py               # Google Sheets integration
│
├── data/                           # Data files
│   ├── careers.csv                 # Career database
│   ├── sample_users.json           # Test data
│   └── history/                    # Export storage
│
├── tests/                          # Test suite
│   ├── test_rule_engine.py         # Rule engine tests
│   ├── test_llm_engine.py          # LLM integration tests
│   ├── test_chatbot_flow.py        # End-to-end tests
│   └── fixtures.json               # Test data
│
└── docs/                           # Documentation
    ├── design_doc.md               # System architecture
    ├── user_manual.md              # User guide
    └── developer_guide.md          # Development guide
```

## 💻 Usage

### Basic Conversation
1. Open the application in your browser
2. Type your career-related question in the chat input
3. Receive personalized advice and recommendations
4. Continue the conversation for more detailed guidance

### Export Conversations
- Click the "Export Chat History" button in the sidebar
- Download your conversation as a JSON file
- Data is also automatically saved to Google Sheets for analytics

### Quick Actions
Use the sidebar buttons for common queries:
- "What career suits my skills?"
- "How do I change careers?"
- "What skills should I develop?"
- "Tell me about job market trends"
- "Help me write a resume"

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=core --cov=utils --cov-report=html

# Run specific test file
pytest tests/test_chatbot_flow.py -v
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-component functionality
- **End-to-End Tests**: Complete conversation flows
- **Performance Tests**: Response time and memory usage

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account and select the repository
4. Set main file path: `app.py`
5. Add secrets in the Streamlit Cloud dashboard
6. Deploy!

### Local Production
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🛠️ Development

### Team Structure
- **Person A**: Framework Lead - Streamlit UI, chatbot orchestration, Google Sheets integration
- **Person B**: Rule Engine - Career database, recommendation logic
- **Person C**: LLM Integration - AI responses, prompt engineering, error handling
- **Person D**: UX Polish - Interface enhancements, testing, deployment

### Development Workflow
1. Create feature branch: `git checkout -b feature/description`
2. Implement changes with tests
3. Run code quality checks: `black . && flake8 .`
4. Submit pull request for review
5. Deploy after approval

### Code Quality
- **Formatting**: Black with 88-character line length
- **Linting**: Flake8 for code quality
- **Type Checking**: MyPy for type safety
- **Testing**: Pytest with coverage reporting

## 🔧 Configuration

### Environment Variables
- `GOOGLE_SHEETS_CREDENTIALS`: Service account JSON (for deployment)
- `GOOGLE_SHEETS_ID`: Spreadsheet identifier
- `DEBUG_MODE`: Enable debug logging and UI elements
- `LOG_LEVEL`: Logging verbosity (INFO, DEBUG, ERROR)

### Customization
- Modify intent patterns in `core/chatbot_framework.py`
- Add new response templates in the `_load_responses()` method
- Customize UI styling in `app.py` CSS section
- Extend career database in `data/careers.csv`

## 📊 Analytics

The system automatically tracks:
- **User Interactions**: Message counts, session duration
- **Intent Distribution**: Popular query types
- **Conversation Patterns**: Common flows and topics
- **Export Usage**: Download frequency and formats

Access analytics data through Google Sheets or the built-in health check.

## 🔍 Troubleshooting

### Common Issues

**Google Sheets Authentication**
```
Error: "Insufficient permissions"
Solution: Ensure service account has edit access to the spreadsheet
```

**Streamlit Session State**
```
Error: Session state not persisting
Solution: Check session_state initialization in app.py
```

**Performance Issues**
```
Error: Slow response times
Solution: Enable caching and optimize Google Sheets calls
```

### Debug Mode
Enable debug mode for detailed logging:
```bash
export DEBUG_MODE=true
streamlit run app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure code quality checks pass
5. Submit a pull request

### Contribution Guidelines
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check `/docs` folder for detailed guides
- **Issues**: Report bugs via GitHub issues
- **Questions**: Contact the development team

## 🎯 Roadmap

### Version 2.0
- [ ] Multi-language support
- [ ] Voice interface integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app companion

### Version 3.0
- [ ] AI-powered resume builder
- [ ] Job market predictions
- [ ] Networking recommendations
- [ ] Career progression tracking

---

Built with ❤️ by the Career Guidance Team

