"""
Simple admin interface for managing users.
Only accessible with admin credentials.
"""

import streamlit as st
from main.utils.supabase_auth import get_supabase_auth, get_current_user, is_authenticated
from datetime import datetime
import json

# Admin credentials (in production, use environment variables)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def is_admin():
    """Check if current user is admin."""
    return get_current_user() == "admin@example.com"

def admin_login():
    """Admin login form."""
    st.title("🔐 Admin Login")
    
    with st.form("admin_login"):
        email = st.text_input("Admin Email")
        password = st.text_input("Admin Password", type="password")
        submit = st.form_submit_button("Login as Admin")
        
        if submit:
            if email == "admin@example.com" and password == ADMIN_PASSWORD:
                # For demo purposes, authenticate as admin
                auth = get_supabase_auth()
                if auth.authenticate(email, password):
                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    st.error("Admin authentication failed")
            else:
                st.error("Invalid admin credentials")

def admin_dashboard():
    """Admin dashboard with user management."""
    st.title("⚙️ Admin Dashboard")
    
    auth = get_supabase_auth()
    
    # User statistics
    st.subheader("📊 User Statistics")
    stats = auth.get_user_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", stats['total_users'])
    
    with col2:
        st.metric("Active Users", stats['active_users'])
    
    with col3:
        st.metric("Demo Users", stats['demo_users'])
    
    st.divider()
    
    # Admin actions
    st.subheader("🛠️ Admin Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clean Demo Users", type="secondary"):
            # Remove demo users older than 24 hours
            demo_users_removed = auth.cleanup_demo_users(1)
            
            if demo_users_removed > 0:
                st.success(f"Removed {demo_users_removed} old demo users.")
            else:
                st.info("No old demo users to remove.")
    
    with col2:
        if st.button("📊 Export User Stats", type="secondary"):
            # Export user statistics
            export_data = {
                **stats,
                'export_date': datetime.now().isoformat()
            }
            
            st.download_button(
                label="📁 Download User Stats",
                data=json.dumps(export_data, indent=2),
                file_name=f"user_stats_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )

# Main admin page
if not is_authenticated():
    admin_login()
elif is_admin():
    admin_dashboard()
else:
    st.error("Access denied. Admin privileges required.")
    st.info("This page is only accessible to administrators.")
