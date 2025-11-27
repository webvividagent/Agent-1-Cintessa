import streamlit as st
from database import db

def init_auth():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None

def show_login():
    st.title("🔐 Agent 1 Cintessa - Login")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                user_id = db.verify_user(username, password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("signup_form"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup_btn = st.form_submit_button("Sign Up")
            
            if signup_btn:
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_username) < 3:
                    st.error("Username must be at least 3 characters")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    user_id = db.create_user(new_username, new_password)
                    if user_id:
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists")

def show_logout():
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.current_session = None
        st.rerun()

def require_auth():
    if st.session_state.user_id is None:
        show_login()
        st.stop()
