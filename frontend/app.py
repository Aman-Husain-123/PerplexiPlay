import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(page_title="PerplexiPlay", page_icon="🎮", layout="wide")

# Session State Initialization
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "username" not in st.session_state:
    st.session_state.username = None

def login(username, password):
    """Login request to FastAPI backend."""
    response = requests.post(
        f"{API_URL}/auth/login",
        data={"username": username, "password": password}
    )
    if response.status_code == 200:
        st.session_state.access_token = response.json()["access_token"]
        st.session_state.username = username
        st.success("Logged in successfully!")
        st.rerun()
    else:
        try:
            error_detail = response.json().get('detail', 'Unknown error')
        except Exception:
            error_detail = f"Server error ({response.status_code})"
        st.error(f"Login failed: {error_detail}")

def register(username, password):
    """Registration request to FastAPI backend."""
    response = requests.post(
        f"{API_URL}/auth/register",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        st.success("Registration successful! Please login.")
    else:
        try:
            error_detail = response.json().get('detail', 'Unknown error')
        except Exception:
            error_detail = f"Server error ({response.status_code})"
        st.error(f"Registration failed: {error_detail}")

def get_me():
    """Fetch current user info using JWT."""
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{API_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def logout():
    """Clear session state."""
    st.session_state.access_token = None
    st.session_state.username = None
    st.rerun()

# --- UI LOGIC ---

if not st.session_state.access_token:
    st.title("🎮 PerplexiPlay")
    st.subheader("Welcome to the Agent Playground")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                login(user, pwd)
    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("Choose Username")
            new_pwd = st.text_input("Choose Password", type="password")
            confirm_pwd = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if new_pwd != confirm_pwd:
                    st.error("Passwords do not match")
                else:
                    register(new_user, new_pwd)
else:
    # Protected Dashboard
    st.sidebar.title(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout()
    
    st.title("🚀 PerplexiPlay Dashboard")
    st.write(f"Welcome back, **{st.session_state.username}**!")
    
    user_info = get_me()
    if user_info:
        with st.expander("👤 User Profile Information"):
            st.json(user_info)
    
    st.divider()
    
    st.info("Phase 1 is complete! The system is ready for Phase 2: Agent Builder.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Agents Created", 0)
    with col2:
        st.metric("Total Executions", 0)
    with col3:
        st.metric("Success Rate", "0%")

    st.subheader("Upcoming Features (Phase 2)")
    st.markdown("""
    - **Agent Builder Interface**: Visual tool to configure AI agents.
    - **Prompt Management**: Centralized repository for agent instructions.
    - **Execution History**: Persistent logs of agent runs and results.
    """)
