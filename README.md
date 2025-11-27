cat > README.md << 'EOF'
# 🤖 Agent 1 Cintessa

A powerful ChatGPT-style AI companion built with Streamlit and Ollama, featuring character customization and user authentication.

![Agent 1 Cintessa](https://img.shields.io/badge/Agent-1_Cintessa-purple)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLMs-green)

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

- Python 3.8+
- [Ollama](https://ollama.ai) installed
- At least one Ollama model (e.g., `ollama pull llama2`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Agent-1-Cintessa.git
   cd Agent-1-Cintessa
