#!/usr/bin/env python3
import streamlit.web.cli as stcli
import sys
import os
import subprocess
import time

def check_ollama():
    """Check if Ollama is running and accessible"""
    try:
        import ollama
        # Try to list models to verify connection
        models = ollama.list()
        print(f"✅ Connected to Ollama. Found {len(models['models'])} models.")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

def start_ollama():
    """Try to start Ollama service"""
    try:
        print("🔄 Attempting to start Ollama service...")
        process = subprocess.Popen(["ollama", "serve"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        # Wait a bit for Ollama to start
        time.sleep(5)
        return process
    except Exception as e:
        print(f"❌ Failed to start Ollama: {e}")
        return None

def main():
    print("🚀 Starting Agent 1 Cintessa...")
    
    # Set the current directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Check if required packages are installed
    try:
        import streamlit
        import ollama
        import bcrypt
        from PIL import Image
        print("✅ All required packages are installed.")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check Ollama connection
    if not check_ollama():
        print("❌ Cannot connect to Ollama. Please make sure Ollama is installed and running.")
        print("💡 You can start it with: ollama serve")
        response = input("Try to start Ollama automatically? (y/n): ").lower()
        if response == 'y':
            ollama_process = start_ollama()
            if ollama_process and check_ollama():
                print("✅ Ollama started successfully!")
            else:
                print("❌ Failed to start Ollama. Please start it manually and try again.")
                sys.exit(1)
        else:
            sys.exit(1)
    
    print("🌐 Starting Streamlit web interface...")
    
    # Run Streamlit with specific configuration
    sys.argv = [
        "streamlit", "run", "app.py", 
        "--server.port=8501", 
        "--server.address=0.0.0.0",
        "--browser.serverAddress=localhost",
        "--theme.base=dark"
    ]
    
    try:
        sys.exit(stcli.main())
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    main()
