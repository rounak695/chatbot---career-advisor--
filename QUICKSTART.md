# 🚀 Quick Start Guide

Get your Career Guidance Chatbot running in minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- OpenAI API key (for AI-powered responses)

## Option 1: Automated Setup (Recommended)

1. **Clone and navigate to the project**
   ```bash
   cd chatbot---career-advisor---2
   ```

2. **Run the automated setup**
   ```bash
   python setup.py
   ```

3. **Configure your API key**
   - Edit `streamlit/secrets.toml`
   - Replace `your-openai-api-key-here` with your actual OpenAI API key

4. **Start the application**
   ```bash
   python run.py
   ```

## Option 2: Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys**
   - Edit `streamlit/secrets.toml`
   - Set your OpenAI API key

3. **Start the application**
   ```bash
   streamlit run app.py
   ```

## What You'll Get

✅ **Interactive Chat Interface** - Clean, responsive UI built with Streamlit  
✅ **Career Recommendations** - Rule-based career suggestions from the database  
✅ **AI-Powered Responses** - Intelligent career advice using OpenAI's GPT models  
✅ **Career Database** - 40+ career paths with detailed information  
✅ **Export Functionality** - Download your chat history  

## Testing the Setup

Run the test script to verify everything is working:
```bash
python test_setup.py
```

## Troubleshooting

### Common Issues

**Import Errors**
- Make sure you've installed requirements: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

**API Key Issues**
- Verify your OpenAI API key is set in `streamlit/secrets.toml`
- Check that the key is valid and has sufficient credits

**Port Already in Use**
- The app runs on port 8501 by default
- Change port: `streamlit run app.py --server.port 8502`

### Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review error messages in the terminal
- Ensure all required files exist in the project structure

## Next Steps

Once running, you can:
- Ask career-related questions in the chat
- Use quick action buttons for common queries
- Export your conversation history
- Explore different career paths and recommendations

Happy career exploring! 🎯
