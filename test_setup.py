#!/usr/bin/env python3
"""
Test script to verify the career guidance chatbot setup
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        from core.chatbot_framework import ChatbotFramework
        print("✅ ChatbotFramework imported successfully")
    except ImportError as e:
        print(f"❌ ChatbotFramework import failed: {e}")
        return False
    
    try:
        from core.rule_engine import RuleEngine
        print("✅ RuleEngine imported successfully")
    except ImportError as e:
        print(f"❌ RuleEngine import failed: {e}")
        return False
    
    try:
        from utils.formatter import format_message
        print("✅ Formatter utilities imported successfully")
    except ImportError as e:
        print(f"❌ Formatter utilities import failed: {e}")
        return False
    
    return True

def test_rule_engine():
    """Test the rule engine functionality"""
    print("\nTesting RuleEngine...")
    
    try:
        from core.rule_engine import RuleEngine
        engine = RuleEngine()
        
        # Test basic recommendations
        response = engine.get_recommendations("What careers should I consider?")
        print("✅ RuleEngine recommendations working")
        print(f"   Sample response: {response[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ RuleEngine test failed: {e}")
        return False

def test_data_files():
    """Test if required data files exist"""
    print("\nTesting data files...")
    
    required_files = [
        "data/careers.csv",
        "requirements.txt",
        "app.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_config_files():
    """Test if configuration files exist"""
    print("\nTesting configuration files...")
    
    config_files = [
        ".streamlit/config.toml",
        "streamlit/secrets.toml"
    ]
    
    all_exist = True
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🚀 Career Guidance Chatbot Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_rule_engine,
        test_data_files,
        test_config_files
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The project is ready to run.")
        print("\nTo start the application:")
        print("1. Set your OpenAI API key in streamlit/secrets.toml")
        print("2. Run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Check file paths and permissions")
        print("- Verify Python version (3.8+)")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
