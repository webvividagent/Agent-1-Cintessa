# 🤖 Agent 1 Cintessa

A powerful ChatGPT-style AI companion built with Streamlit and Ollama, featuring character customization and user authentication.

![Agent 1 Cintessa](https://img.shields.io/badge/Agent-1_Cintessa-purple)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLMs-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🎨 **Character Image System** - Swap character pictures from the `character_images/` folder
- 🤖 **Multiple AI Models** - Support for Ollama models (JOSIEFIED-Qwen3, Llama2, Mistral, etc.)
- 💬 **ChatGPT-style Interface** - Familiar sidebar with chat history
- 🔐 **User Authentication** - Login/signup system with persistent sessions
- 🎯 **Custom System Prompts** - Override AI personality per chat
- 🖼️ **Background Selector** - Choose from background images
- 📋 **Copy Buttons** - Easy message copying
- 🎨 **High Contrast Theme** - Black background with light purple text
- 💾 **Persistent Memory** - Remembers user details and preferences

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **Ollama** - Follow installation instructions at [ollama.ai](https://ollama.ai)
- **Git** - To clone the repository

### Step-by-Step Installation

#### 1. Install Ollama (if not already installed)

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh

macOS:
bash

brew install ollama

Windows:
Download from ollama.ai
2. Download an AI Model
bash

# Start Ollama service
ollama serve

# In a new terminal, download a model (choose one):
ollama pull llama2
# OR
ollama pull mistral
# OR
ollama pull goekdenizguelmez/JOSIEFIED-Qwen3:0.6b

3. Clone and Setup Agent 1 Cintessa
bash

# Clone the repository
git clone https://github.com/webvividagent/Agent-1-Cintessa.git
cd Agent-1-Cintessa

# Make the run script executable
chmod +x run.sh

# Run the automated setup (recommended for first-time users)
./run.sh

The ./run.sh script will automatically:

    Create a Python virtual environment

    Install all required dependencies

    Check for Ollama models

    Launch the application

4. Manual Installation (Alternative)

If you prefer manual setup:
bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

First Run

    The application will automatically open in your browser at http://localhost:8501

    Create an account or login if you already have one

    Add character images (see Customization section below)

    Start chatting with Agent 1 Cintessa!

🎨 Customization
Adding Character Images

    Place character images in the character_images/ folder

    Supported formats: PNG, JPG, JPEG, GIF

    Use the sidebar dropdown to switch between characters during chat

Example:
bash

# Add your character images
cp /path/to/your/character.png character_images/
cp /path/to/another/character.jpg character_images/

Adding Background Images

    Place background images in the background_images/ folder

    Select them from the sidebar background selector

Custom System Prompts

Modify the AI's personality for each chat session using the system prompt in the sidebar. Examples:

    "You are a helpful AI assistant specializing in coding"

    "You are a creative writer who speaks in Shakespearean English"

    "You are a sarcastic but knowledgeable tech expert"

📁 Project Structure
text

Agent-1-Cintessa/
├── app.py                 # Main Streamlit application
├── auth.py               # Authentication system
├── database.py           # SQLite database operations
├── run.py               # Application launcher
├── run.sh               # Automated setup and launch script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── character_images/   # Character image storage
│   └── README.txt
└── background_images/  # Background image storage
    └── README.txt

🔧 Configuration
Environment Variables

Create a .env file from the template:
bash

cp .env.example .env

Edit the .env file:
env

OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=goekdenizguelmez/JOSIEFIED-Qwen3:0.6b

Available Models

The app automatically detects all installed Ollama models. To see available models:
bash

ollama list

To add more models:
bash

ollama pull codellama
ollama pull phi
ollama pull neural-chat

🛠️ Development
Running in Development Mode
bash

source venv/bin/activate
streamlit run app.py --server.port=8501

Database

The app uses SQLite for data persistence. The database file (agent1.db) is created automatically in the project directory.
Testing Ollama Connection
bash

python test_ollama.py

❓ Troubleshooting
Common Issues

"Ollama connection failed"

    Ensure Ollama is running: ollama serve

    Check service status: curl http://localhost:11434/api/tags

"No models available"

    Download a model: ollama pull llama2

    Verify models: ollama list

"Port 8501 already in use"

    Use a different port: streamlit run app.py --server.port=8502

    Kill existing process: pkill -f streamlit

Python package errors

    Recreate virtual environment: rm -rf venv && python3 -m venv venv

    Reinstall dependencies: pip install -r requirements.txt

Getting Help

If you encounter issues:

    Check the Ollama documentation

    Check the Streamlit documentation

    Create an issue on GitHub

🤝 Contributing

We welcome contributions! Here's how to help:

    Fork the repository

    Create a feature branch: git checkout -b feature/amazing-feature

    Commit your changes: git commit -m 'Add amazing feature'

    Push to the branch: git push origin feature/amazing-feature

    Open a Pull Request

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

    Built with Streamlit

    AI powered by Ollama

    Icons from Twemoji

    Character system inspired by modern AI chat interfaces

Happy chatting! 🎉 If you enjoy Agent 1 Cintessa, please give it a ⭐ on GitHub!
EOF
text


Now commit and push the improved README:

```bash
git add README.md
git commit -m "Add comprehensive installation instructions and troubleshooting guide"
git push origin main

This new README includes:

✅ Step-by-step installation for all platforms
✅ Detailed Ollama setup instructions
✅ Troubleshooting section for common issues
✅ Better formatting with badges and clear sections
✅ Examples for character images and system prompts
✅ Development instructions for contributors
✅ Visual project structure tree
