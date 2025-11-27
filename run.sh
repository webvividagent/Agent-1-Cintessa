#!/bin/bash

# run.sh - Complete launcher for Agent 1 Cintessa

echo "🤖 Starting Agent 1 Cintessa..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Make sure you're in the agent1_cintessa directory."
    exit 1
fi

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements if not already installed
if ! python -c "import streamlit" &> /dev/null; then
    echo "📚 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if Ollama is running
echo "🔍 Checking Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama is not running. Starting Ollama service..."
    # Start Ollama in the background
    ollama serve &
    OLLAMA_PID=$!
    echo "📥 Started Ollama with PID: $OLLAMA_PID"
    # Wait for Ollama to start
    sleep 5
fi

# Check if JOSIEFIED-Qwen3 model exists
echo "🔍 Checking for JOSIEFIED-Qwen3 model..."
if ! ollama list | grep -q "JOSIEFIED-Qwen3"; then
    echo "📥 Pulling JOSIEFIED-Qwen3 model..."
    ollama pull goekdenizguelmez/JOSIEFIED-Qwen3:0.6b
else
    echo "✅ JOSIEFIED-Qwen3 model found!"
fi

# Kill any existing Streamlit processes on port 8501
echo "🔄 Cleaning up any existing processes..."
pkill -f "streamlit run app.py" 2>/dev/null || true
sleep 2

# Run the application
echo "🌐 Launching Agent 1 Cintessa..."
echo "=========================================="
echo "📱 The app will open at: http://localhost:8501"
echo "📱 Alternative URL: http://127.0.0.1:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo "=========================================="
echo ""

# Run the app
python run.py

# Cleanup: if we started Ollama, kill it when Streamlit exits
if [ ! -z "$OLLAMA_PID" ]; then
    echo "🛑 Stopping Ollama service..."
    kill $OLLAMA_PID
fi
