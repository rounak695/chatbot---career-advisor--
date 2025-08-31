#!/usr/bin/env python3
"""
Setup script for Career Guidance Chatbot
"""

import os
import sys
import subprocess
import shutil

def install_requirements():
    """Install required packages from requirements.txt"""
    print("📦 Installing required packages...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories if they don't exist"""
    print("📁 Creating necessary directories...")
    
    directories = [
        ".streamlit",
        "data/history",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_secrets():
    """Set up secrets file if it doesn't exist"""
    print("🔐 Setting up secrets configuration...")
    
    secrets_file = "streamlit/secrets.toml"
    if not os.path.exists(secrets_file):
        print("⚠️  secrets.toml not found. Please create it manually.")
        print("   See README.md for configuration instructions.")
        return False
    
    print("✅ Secrets file found")
    return True

def check_data_files():
    """Check if data files exist"""
    print("📊 Checking data files...")
    
    data_files = [
        "data/careers.csv"
    ]
    
    all_exist = True
    for data_file in data_files:
        if os.path.exists(data_file):
            print(f"✅ {data_file} exists")
        else:
            print(f"❌ {data_file} missing")
            all_exist = False
    
    return all_exist

def run_tests():
    """Run basic tests to verify setup"""
    print("🧪 Running basic tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_setup.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Basic tests passed")
            return True
        else:
            print("❌ Basic tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def main():
    """Main setup function"""
    print("🎯 Career Guidance Chatbot Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Run setup steps
    steps = [
        install_requirements,
        create_directories,
        setup_secrets,
        check_data_files,
        run_tests
    ]
    
    all_passed = True
    for step in steps:
        print()
        if not step():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\nTo start the application:")
        print("1. Set your OpenAI API key in streamlit/secrets.toml")
        print("2. Run: python run.py")
        print("   or: streamlit run app.py")
    else:
        print("⚠️  Setup completed with some issues.")
        print("Please check the errors above and resolve them.")
        print("\nFor help, check README.md")

if __name__ == "__main__":
    main()
