import streamlit as st
from main.utils.supabase_auth import get_supabase_auth, get_current_user, is_authenticated
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Supabase authentication
@st.cache_resource
def init_supabase_auth():
    """Initialize Supabase authentication system."""
    return get_supabase_auth()

def show_auth_page():
    """Show authentication page with login/register options."""
    st.title("🌱 Emission Calculator")
    st.markdown("Track your carbon footprint and make a difference!")
    
    # Initialize auth system
    auth = init_supabase_auth()
    
    # Tab selection
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("🔐 Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if email and password:
                    if auth.authenticate(email, password):
                        st.success("Login successful! 🎉")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("📝 Register")
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Register")
            
            if register_button:
                if username and email and password and confirm_password:
                    if password == confirm_password:
                        if auth.register_user(email, password, username):
                            st.success("Registration successful! Please login.")
                        else:
                            st.error("Registration failed. Please try again.")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")

# Initialize authentication
auth_system = init_supabase_auth()

# Check if user is authenticated
if not is_authenticated():
    show_auth_page()
else:
    # User is authenticated, show main app
    
    # Add user info and logout in sidebar
    with st.sidebar:
        current_user = get_current_user()
        if current_user:
            st.markdown(f"👤 **Welcome, {current_user}!**")
            if st.button("Logout", type="secondary"):
                auth_system.logout()
                st.rerun()
    
    # Define pages
    home = st.Page(
        "overview/home.py", title="Home", icon="🏠", default=True,
    )

    transport = st.Page(
        "categories/transport.py", title="Transport", icon="🚗",
    )
    energy = st.Page(
        "categories/energy.py", title="Energy", icon="⚡",
    )
    food = st.Page(
        "categories/enhanced_food.py", title="Food", icon="🥗",
    )

    goals = st.Page(
        "categories/goals_tracking.py", title="Goals & Progress", icon="🎯",
    )

    results = st.Page(
        "results/enhanced_analytics.py", title="Results & Analytics", icon="📊",
    )
    
    profile = st.Page(
        "profile/user_profile.py", title="Profile", icon="👤",
    )

    pg = st.navigation(
        {
            "Overview": [home],
            "Categories": [transport, energy, food],
            "Goals": [goals],
            "Results": [results],
            "Account": [profile],
        }
    )

    pg.run()