"""
Authentication utilities for the emission calculator app.
Simple user authentication with password hashing and session management.
"""

import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from pathlib import Path

class SimpleAuth:
    """Simple authentication system using local file storage."""
    
    def __init__(self, users_file: str = "users.json"):
        self.users_file = Path(users_file)
        self.users = self._load_users()
    
    def _load_users(self) -> Dict:
        """Load users from file or create empty dict."""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_users(self):
        """Save users to file."""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt."""
        salt = "emission_calculator_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str = "") -> bool:
        """Register a new user."""
        if username in self.users:
            return False
        
        self.users[username] = {
            "password_hash": self._hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "settings": {
                "units": "metric",
                "language": "en",
                "notifications": True
            }
        }
        self._save_users()
        return True
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials."""
        if username not in self.users:
            return False
        
        stored_hash = self.users[username]["password_hash"]
        password_hash = self._hash_password(password)
        
        if stored_hash == password_hash:
            # Update last login
            self.users[username]["last_login"] = datetime.now().isoformat()
            self._save_users()
            return True
        
        return False
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        return username in self.users
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information."""
        if username in self.users:
            user_data = self.users[username].copy()
            user_data.pop('password_hash', None)  # Don't return password hash
            return user_data
        return None
    
    def update_user_settings(self, username: str, settings: Dict) -> bool:
        """Update user settings."""
        if username not in self.users:
            return False
        
        self.users[username]["settings"].update(settings)
        self._save_users()
        return True

# Streamlit authentication functions
def init_auth_session():
    """Initialize authentication session state."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'auth_system' not in st.session_state:
        st.session_state.auth_system = SimpleAuth()

def login_form():
    """Display login form."""
    st.subheader("🔐 Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username and password:
                auth = st.session_state.auth_system
                if auth.authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")

def register_form():
    """Display registration form."""
    st.subheader("📝 Register")
    
    with st.form("register_form"):
        username = st.text_input("Choose Username")
        email = st.text_input("Email (optional)")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if not username or not password:
                st.warning("Username and password are required")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                auth = st.session_state.auth_system
                if auth.user_exists(username):
                    st.error("Username already exists")
                else:
                    if auth.register_user(username, password, email):
                        st.success("Registration successful! You can now login.")
                        st.balloons()
                    else:
                        st.error("Registration failed. Please try again.")

def logout():
    """Logout user."""
    st.session_state.authenticated = False
    st.session_state.username = None
    # Clear user-specific session data
    keys_to_clear = [
        'transport_emissions', 'energy_emissions', 'food_emissions',
        'carbon_goals', 'progress_data'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def require_auth(func):
    """Decorator to require authentication for a function."""
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.warning("Please login to access this feature.")
            return None
        return func(*args, **kwargs)
    return wrapper

def show_auth_page():
    """Show authentication page with login/register tabs."""
    st.title("🌍 Carbon Emissions Calculator")
    st.markdown("""
        Welcome to the Carbon Emissions Calculator! 
        Please login or register to start tracking your carbon footprint.
    """)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        login_form()
    
    with tab2:
        register_form()
    
    st.divider()
    
    st.markdown("""
        ### Why create an account?
        - 📊 **Track your progress** over time
        - 🎯 **Set and monitor goals** for emission reduction
        - 💾 **Save your data** securely
        - 📈 **View historical trends** and improvements
        - 🌱 **Get personalized recommendations**
    """)
    
    # Demo account option
    st.markdown("---")
    st.markdown("### 🚀 Quick Start")
    st.markdown("Want to try without creating an account?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Demo Account", type="primary"):
            demo_username = f"demo_{int(datetime.now().timestamp())}"
            auth = st.session_state.auth_system
            if auth.register_user(demo_username, "demo123", "demo@example.com"):
                if auth.authenticate(demo_username, "demo123"):
                    st.session_state.authenticated = True
                    st.session_state.username = demo_username
                    st.success("Demo account created! You're now logged in.")
                    st.rerun()
    
    with col2:
        st.markdown("**Demo account includes:**")
        st.markdown("- All calculator features")
        st.markdown("- Goal tracking")
        st.markdown("- Progress monitoring")
        st.markdown("- Temporary data storage")

def get_current_user() -> Optional[str]:
    """Get current authenticated user."""
    return st.session_state.get('username')

def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get('authenticated', False)
