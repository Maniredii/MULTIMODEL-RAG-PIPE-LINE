import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

def signup():
    st.title("Sign Up")
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        username = st.text_input("Username")
        signup_button = st.form_submit_button("Create Account")
        
        if signup_button:
            try:
                # Create user in Supabase
                response = supabase.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "username": username
                        }
                    }
                })
                
                if response.user:
                    st.success("Account created successfully! Please check your email to verify your account.")
                    st.session_state.user = response.user
                    return True
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    return False

def login():
    st.title("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        
        if login_button:
            try:
                # Sign in with Supabase
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                if response.user:
                    st.success("Logged in successfully!")
                    st.session_state.user = response.user
                    return True
                    
            except Exception as e:
                st.error("Invalid email or password")
    return False

def auth_page():
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Center the login/signup container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <style>
                .auth-container {
                    background-color: #f0f2f6;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .stButton button {
                    width: 100%;
                }
            </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            tab1, tab2 = st.tabs(["Login", "Sign Up"])
            
            with tab1:
                if login():
                    st.rerun()
            
            with tab2:
                if signup():
                    st.rerun() 