#!/usr/bin/env python3
"""
Simple startup script for the Career Guidance Chatbot
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def check_config():
    """Check if configuration files exist"""
    config_files = [
        "streamlit/secrets.toml",
        ".streamlit/config.toml"
    ]
    
    missing_configs = []
    for config_file in config_files:
        if not os.path.exists(config_file):
            missing_configs.append(config_file)
            print(f"❌ {config_file} is missing")
        else:
            print(f"✅ {config_file} exists")
    
    if missing_configs:
        print("\n⚠️  Some configuration files are missing.")
        print("The application may not work properly without proper configuration.")
        print("Please check the README.md for setup instructions.")
    
    return len(missing_configs) == 0

def start_application():
    """Start the Streamlit application"""
    print("\n🚀 Starting Career Guidance Chatbot...")
    print("The application will open in your default web browser.")
    print("Press Ctrl+C to stop the application.\n")
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main function"""
    print("🎯 Career Guidance Chatbot Setup")
    print("=" * 40)
    
    # Run checks
    checks = [
        check_python_version,
        check_dependencies,
        check_config
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    if all_passed:
        print("✅ All checks passed!")
        start_application()
    else:
        print("⚠️  Some checks failed. Please resolve the issues above.")
        print("\nTo manually start the application:")
        print("streamlit run app.py")
        
        print("\nFor help, check:")
        print("- README.md for setup instructions")
        print("- requirements.txt for dependencies")
        print("- streamlit/secrets.toml for configuration")

if __name__ == "__main__":
    main()
