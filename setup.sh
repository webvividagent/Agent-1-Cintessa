#!/bin/bash
echo "Setting up Agent 1 Cintessa..."
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Checking for Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Please install Ollama from https://ollama.ai"
    exit 1
fi

echo "Checking for JOSIEFIED-Qwen3 model..."
if ollama list | grep -q "JOSIEFIED-Qwen3"; then
    echo "JOSIEFIED-Qwen3 model already exists!"
else
    echo "Pulling JOSIEFIED-Qwen3 model..."
    ollama pull goekdenizguelmez/JOSIEFIED-Qwen3:0.6b
fi

echo "Setup complete!"
echo "To run the application:"
echo "  python run.py"
echo "or"
echo "  streamlit run app.py"
