#!/usr/bin/env python3
"""
Comprehensive verification script for Career Guidance Chatbot
"""

import os
import sys
import importlib
import traceback

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")

def test_core_modules():
    """Test all core modules"""
    print_section("Testing Core Modules")
    
    core_modules = [
        ("core.chatbot_framework", "ChatbotFramework"),
        ("core.rule_engine", "RuleEngine"),
        ("core.llm_engine", "LLMEngine"),
        ("core.prompts", "CAREER_ADVISOR_PROMPT")
    ]
    
    results = {}
    for module_path, class_name in core_modules:
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, class_name):
                # Try to instantiate if it's a class
                if class_name in ["ChatbotFramework", "RuleEngine", "LLMEngine"]:
                    try:
                        if class_name == "ChatbotFramework":
                            instance = getattr(module, class_name)()
                        elif class_name == "RuleEngine":
                            instance = getattr(module, class_name)()
                        elif class_name == "LLMEngine":
                            # LLMEngine requires OpenAI API key, so just test import
                            pass
                        print(f"✅ {module_path}.{class_name} - OK")
                        results[module_path] = True
                    except Exception as e:
                        if "OPENAI_API_KEY" in str(e):
                            print(f"⚠️  {module_path}.{class_name} - OK (requires API key)")
                            results[module_path] = True
                        else:
                            print(f"❌ {module_path}.{class_name} - Failed: {e}")
                            results[module_path] = False
                else:
                    print(f"✅ {module_path}.{class_name} - OK")
                    results[module_path] = True
            else:
                print(f"❌ {module_path}.{class_name} - Not found")
                results[module_path] = False
        except Exception as e:
            print(f"❌ {module_path} - Import failed: {e}")
            results[module_path] = False
    
    return results

def test_utility_modules():
    """Test utility modules"""
    print_section("Testing Utility Modules")
    
    utility_modules = [
        ("utils.formatter", "format_message"),
        ("utils.errors", "LLMResponseError"),
        ("utils.sheets_api", "SheetsAPI")
    ]
    
    results = {}
    for module_path, function_name in utility_modules:
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, function_name):
                print(f"✅ {module_path}.{function_name} - OK")
                results[module_path] = True
            else:
                print(f"❌ {module_path}.{function_name} - Not found")
                results[module_path] = False
        except Exception as e:
            print(f"❌ {module_path} - Import failed: {e}")
            results[module_path] = False
    
    return results

def test_data_files():
    """Test data files and structure"""
    print_section("Testing Data Files")
    
    required_files = [
        "data/careers.csv",
        "requirements.txt",
        "app.py",
        "README.md",
        "QUICKSTART.md"
    ]
    
    optional_files = [
        "streamlit/secrets.toml",
        ".streamlit/config.toml",
        "setup.py",
        "run.py",
        "test_setup.py"
    ]
    
    results = {"required": {}, "optional": {}}
    
    print("Required files:")
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
            results["required"][file_path] = True
        else:
            print(f"❌ {file_path} - MISSING")
            results["required"][file_path] = False
    
    print("\nOptional files:")
    for file_path in optional_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
            results["optional"][file_path] = True
        else:
            print(f"⚠️  {file_path} - Missing (optional)")
            results["optional"][file_path] = False
    
    return results

def test_functionality():
    """Test basic functionality"""
    print_section("Testing Basic Functionality")
    
    try:
        from core.chatbot_framework import ChatbotFramework
        from core.rule_engine import RuleEngine
        
        # Test rule engine
        rule_engine = RuleEngine()
        response = rule_engine.get_recommendations("test query")
        if response and len(response) > 0:
            print("✅ RuleEngine recommendations working")
        else:
            print("❌ RuleEngine returned empty response")
            return False
        
        # Test chatbot framework
        chatbot = ChatbotFramework()
        if hasattr(chatbot, 'process_message'):
            print("✅ ChatbotFramework initialized successfully")
        else:
            print("❌ ChatbotFramework missing process_message method")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        traceback.print_exc()
        return False

def generate_report(core_results, utility_results, data_results, functionality_ok):
    """Generate final status report"""
    print_header("FINAL STATUS REPORT")
    
    # Core modules status
    core_passed = sum(core_results.values())
    core_total = len(core_results)
    print(f"Core Modules: {core_passed}/{core_total} passed")
    
    # Utility modules status
    utility_passed = sum(utility_results.values())
    utility_total = len(utility_results)
    print(f"Utility Modules: {utility_passed}/{utility_total} passed")
    
    # Data files status
    required_passed = sum(data_results["required"].values())
    required_total = len(data_results["required"])
    print(f"Required Files: {required_passed}/{required_total} present")
    
    # Overall status
    total_tests = core_total + utility_total + required_total + 1  # +1 for functionality
    passed_tests = core_passed + utility_passed + required_passed + (1 if functionality_ok else 0)
    
    print(f"\nOverall Status: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 EXCELLENT! Your Career Guidance Chatbot is ready to run!")
        print("\nNext steps:")
        print("1. Set your OpenAI API key in streamlit/secrets.toml")
        print("2. Run: python run.py")
        print("   or: streamlit run app.py")
        print("\nFor help, see QUICKSTART.md")
    elif passed_tests >= total_tests * 0.8:
        print("\n✅ GOOD! Most components are working.")
        print("Check the warnings above and resolve any issues.")
        print("The application should work with basic functionality.")
    else:
        print("\n⚠️  ATTENTION! Several components have issues.")
        print("Please resolve the errors above before running the application.")
        print("Check README.md and QUICKSTART.md for help.")

def main():
    """Main verification function"""
    print_header("CAREER GUIDANCE CHATBOT VERIFICATION")
    
    print("This script will verify all components of your Career Guidance Chatbot setup.")
    print("Make sure you're in the project directory before running.")
    
    # Run all tests
    core_results = test_core_modules()
    utility_results = test_utility_modules()
    data_results = test_data_files()
    functionality_ok = test_functionality()
    
    # Generate report
    generate_report(core_results, utility_results, data_results, functionality_ok)

if __name__ == "__main__":
    main()
