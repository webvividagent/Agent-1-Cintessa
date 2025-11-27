import streamlit as st
import ollama
import os
import base64
from PIL import Image
import io
from database import db
import auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize authentication
auth.init_auth()

# Page configuration
st.set_page_config(
    page_title="Agent 1 Cintessa",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High Contrast Dark Theme with Light Purple Text
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #000000 !important;
        color: #E0B0FF !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #111111 !important;
        border-right: 1px solid #4A1E7F !important;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        color: #C77DFF !important;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 0 0 10px #C77DFF;
    }
    
    /* Text elements */
    .stMarkdown, .stText, .stTitle, .stHeader {
        color: #E0B0FF !important;
    }
    
    /* Chat messages */
    .message-user {
        background-color: #1A1A1A !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #8A2BE2;
        color: #E0B0FF !important;
        border: 1px solid #4A1E7F !important;
    }
    
    .message-assistant {
        background-color: #1A1A1A !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9370DB;
        color: #E0B0FF !important;
        border: 1px solid #4A1E7F !important;
    }
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea {
        background-color: #111111 !important;
        color: #E0B0FF !important;
        border: 1px solid #4A1E7F !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #4A1E7F !important;
        color: #E0B0FF !important;
        border: 1px solid #8A2BE2 !important;
        font-weight: bold;
    }
    
    .stButton button:hover {
        background-color: #5D2A9E !important;
        border: 1px solid #9370DB !important;
    }
    
    /* Select boxes */
    .stSelectbox select {
        background-color: #111111 !important;
        color: #E0B0FF !important;
        border: 1px solid #4A1E7F !important;
    }
    
    /* Sidebar text */
    .css-1aumxhk {
        color: #E0B0FF !important;
    }
    
    /* Character image */
    .character-image {
        border-radius: 50%;
        border: 3px solid #8A2BE2;
        box-shadow: 0 0 15px #8A2BE2;
    }
    
    /* Copy button */
    .stButton button[kind="secondary"] {
        background-color: #2D1B4E !important;
        color: #E0B0FF !important;
        border: 1px solid #8A2BE2 !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #1A2A1A !important;
        color: #90EE90 !important;
        border: 1px solid #32CD32 !important;
    }
    
    /* Error messages */
    .stError {
        background-color: #2A1A1A !important;
        color: #FFB6C1 !important;
        border: 1px solid #FF69B4 !important;
    }
    
    /* Chat input */
    .stChatInput input {
        background-color: #111111 !important;
        color: #E0B0FF !important;
        border: 1px solid #4A1E7F !important;
    }
</style>
""", unsafe_allow_html=True)

def get_available_models():
    """Get all available Ollama models with robust error handling"""
    try:
        models_response = ollama.list()
        
        if isinstance(models_response, dict) and 'models' in models_response:
            models = [model['name'] for model in models_response['models']]
            return models
        elif isinstance(models_response, list):
            models = [model['name'] for model in models_response]
            return models
        else:
            return ['goekdenizguelmez/JOSIEFIED-Qwen3:0.6b', 'llama2', 'mistral']
            
    except Exception as e:
        print(f"Error fetching models: {e}")
        return ['goekdenizguelmez/JOSIEFIED-Qwen3:0.6b', 'llama2', 'mistral']

def get_character_images():
    if not os.path.exists('character_images'):
        os.makedirs('character_images')
    images = [f for f in os.listdir('character_images') 
              if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return images if images else ['default.png']

def get_background_images():
    if not os.path.exists('background_images'):
        os.makedirs('background_images')
    return [f for f in os.listdir('background_images') 
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

def init_session_state():
    if 'current_session' not in st.session_state:
        st.session_state.current_session = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'model' not in st.session_state:
        default_model = os.getenv('DEFAULT_MODEL', 'goekdenizguelmez/JOSIEFIED-Qwen3:0.6b')
        st.session_state.model = default_model
    if 'models_loaded' not in st.session_state:
        st.session_state.models_loaded = False
    if 'available_models' not in st.session_state:
        st.session_state.available_models = []
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = ""

def create_new_chat():
    user_id = st.session_state.user_id
    session_id = db.create_chat_session(user_id)
    st.session_state.current_session = session_id
    st.session_state.messages = []
    st.session_state.system_prompt = ""
    st.rerun()

def load_chat_session(session_id):
    st.session_state.current_session = session_id
    messages = db.get_session_messages(session_id)
    st.session_state.messages = [{'role': role, 'content': content} for role, content, _ in messages]
    
    # Load the system prompt for this session
    sessions = db.get_user_sessions(st.session_state.user_id)
    for session in sessions:
        if session[0] == session_id:
            st.session_state.system_prompt = session[3] if session[3] else ""
            break

def get_current_session_details():
    if st.session_state.current_session:
        sessions = db.get_user_sessions(st.session_state.user_id)
        for session in sessions:
            if session[0] == st.session_state.current_session:
                return session
    return None

def main():
    auth.require_auth()
    
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, {st.session_state.username}!")
        auth.show_logout()
        
        st.markdown("---")
        
        # New Chat button
        if st.button("➕ New Chat", use_container_width=True):
            create_new_chat()
        
        st.markdown("### Chat History")
        sessions = db.get_user_sessions(st.session_state.user_id)
        
        for session in sessions:
            session_id, title, created_at, system_prompt, character_image = session
            btn_label = f"💬 {title}"
            if st.button(btn_label, key=f"session_{session_id}", use_container_width=True):
                load_chat_session(session_id)
        
        st.markdown("---")
        
        # Model selection
        st.markdown("### AI Model")
        
        if st.button("🔄 Refresh Models", use_container_width=True):
            st.session_state.models_loaded = False
            st.session_state.available_models = []
            st.rerun()
        
        # Load models
        if not st.session_state.models_loaded or not st.session_state.available_models:
            available_models = get_available_models()
            st.session_state.available_models = available_models
            st.session_state.models_loaded = True
        else:
            available_models = st.session_state.available_models
        
        # Model selection dropdown
        if available_models:
            current_model = st.session_state.model
            if current_model in available_models:
                default_index = available_models.index(current_model)
            else:
                default_index = 0
            
            selected_model = st.selectbox(
                "Select Model:",
                available_models,
                index=default_index,
                key="model_selector"
            )
            
            if selected_model != st.session_state.model:
                st.session_state.model = selected_model
                st.success(f"✅ Model changed to: {selected_model}")
        
        # Character image selector
        st.markdown("### Character Image")
        character_images = get_character_images()
        current_session = get_current_session_details()
        current_character = current_session[4] if current_session else 'default.png'
        
        selected_character = st.selectbox(
            "Choose character",
            character_images,
            index=character_images.index(current_character) if current_character in character_images else 0,
            key="character_selector"
        )
        
        if st.session_state.current_session and selected_character != current_character:
            db.update_session_character(st.session_state.current_session, selected_character)
            st.rerun()
        
        # System prompt - FIXED: Use session_state to track changes
        st.markdown("### System Prompt")
        system_prompt = st.text_area(
            "Custom system prompt for this chat",
            value=st.session_state.system_prompt,
            height=150,
            key="system_prompt_input"
        )
        
        # Update system prompt in session state when user types
        if system_prompt != st.session_state.system_prompt:
            st.session_state.system_prompt = system_prompt
        
        # Save system prompt button
        if st.button("💾 Save System Prompt", use_container_width=True) and st.session_state.current_session:
            db.update_session_system_prompt(st.session_state.current_session, system_prompt)
            st.success("✅ System prompt updated!")
            st.session_state.system_prompt = system_prompt
    
    # Main chat area
    st.markdown('<div class="main-header">🤖 AGENT 1 CINTESSA</div>', unsafe_allow_html=True)
    
    # Display current model info
    st.markdown(f"**Current Model:** `{st.session_state.model}`")
    
    # Display current system prompt preview
    if st.session_state.system_prompt:
        with st.expander("📝 Current System Prompt"):
            st.text(st.session_state.system_prompt[:200] + "..." if len(st.session_state.system_prompt) > 200 else st.session_state.system_prompt)
    
    # Display character image if available
    if current_session:
        character_image = current_session[4]
        character_path = os.path.join('character_images', character_image)
        if os.path.exists(character_path):
            st.image(character_path, width=100, caption="Current Character", use_column_width=False)
    
    # Chat messages display
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="message-user">
                    <strong>👤 YOU:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    st.markdown(f"""
                    <div class="message-assistant">
                        <strong>🤖 CINTESSA:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("📋", key=f"copy_{i}"):
                        st.code(message['content'])
    
    # Auto-scroll
    if len(st.session_state.messages) > 0:
        st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)
    
    # Chat input - FIXED: Check if we have a current session
    st.markdown("---")
    
    if not st.session_state.current_session:
        st.warning("⚠️ Please create a new chat or select an existing one from the sidebar.")
    else:
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            # Add user message
            st.session_state.messages.append({'role': 'user', 'content': user_input})
            db.add_message(st.session_state.current_session, 'user', user_input)
            
            # Get the current system prompt
            system_prompt = st.session_state.system_prompt
            
            # Prepare messages for Ollama
            messages = []
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            messages.extend(st.session_state.messages)
            
            # Get AI response
            with st.spinner("Cintessa is thinking..."):
                try:
                    response = ollama.chat(
                        model=st.session_state.model,
                        messages=messages,
                        stream=False
                    )
                    ai_response = response['message']['content']
                    
                    # Add AI response
                    st.session_state.messages.append({'role': 'assistant', 'content': ai_response})
                    db.add_message(st.session_state.current_session, 'assistant', ai_response)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error getting response: {str(e)}")

if __name__ == "__main__":
    main()
