"""
Supabase authentication and database integration.
This replaces the current SQLite database_auth.py
"""

import os
from supabase import create_client, Client
from typing import Optional, Dict, Any
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseAuth:
    """Supabase authentication and database manager."""
    
    def __init__(self):
        """Initialize Supabase client."""
        # Get environment variables
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file.")
        
        self.client: Client = create_client(supabase_url, supabase_key)
    
    def register_user(self, email: str, password: str, username: str) -> bool:
        """Register a new user with Supabase Auth."""
        try:
            # Register with Supabase Auth
            auth_response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username
                    }
                }
            })
            
            if auth_response.user:
                # Store user info in session
                st.session_state.user = auth_response.user
                st.session_state.authenticated = True
                return True
            return False
            
        except Exception as e:
            st.error(f"Registration failed: {str(e)}")
            return False
    
    def authenticate(self, email: str, password: str) -> bool:
        """Authenticate user with Supabase."""
        try:
            auth_response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if auth_response.user:
                # Store user info in session
                st.session_state.user = auth_response.user
                st.session_state.authenticated = True
                return True
            return False
            
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return False
    
    def logout(self):
        """Logout user."""
        try:
            self.client.auth.sign_out()
            st.session_state.authenticated = False
            st.session_state.user = None
            return True
        except Exception as e:
            st.error(f"Logout failed: {str(e)}")
            return False
    
    def get_current_user(self) -> Optional[str]:
        """Get current authenticated user email."""
        user = st.session_state.get('user')
        if user and hasattr(user, 'email'):
            return user.email
        return None
    
    def get_current_user_id(self) -> Optional[str]:
        """Get current authenticated user ID."""
        user = st.session_state.get('user')
        if user and hasattr(user, 'id'):
            return user.id
        return None
    
    def save_user_emissions(self, category: str, emissions: float, details: Dict[str, Any]) -> bool:
        """Save user emissions to Supabase."""
        try:
            user_id = self.get_current_user_id()
            if not user_id:
                st.error("User not authenticated")
                return False
            
            self.client.table('user_emissions').insert({
                'user_id': user_id,
                'category': category,
                'emissions': emissions,
                'details': details,
                'created_at': datetime.now().isoformat()
            }).execute()
            return True
        except Exception as e:
            st.error(f"Failed to save emissions: {str(e)}")
            return False
    
    def get_user_emissions(self) -> list:
        """Get current user's emission history."""
        try:
            user_id = self.get_current_user_id()
            if not user_id:
                return []
            
            response = self.client.table('user_emissions').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Failed to get emissions: {str(e)}")
            return []
    
    def save_user_goals(self, goals: Dict[str, Any]) -> bool:
        """Save user goals to Supabase."""
        try:
            user_id = self.get_current_user_id()
            if not user_id:
                st.error("User not authenticated")
                return False
            
            # Upsert goals (update if exists, insert if not)
            self.client.table('user_goals').upsert({
                'user_id': user_id,
                'goals': goals,
                'updated_at': datetime.now().isoformat()
            }).execute()
            return True
        except Exception as e:
            st.error(f"Failed to save goals: {str(e)}")
            return False
    
    def get_user_goals(self) -> Dict[str, Any]:
        """Get current user's goals."""
        try:
            user_id = self.get_current_user_id()
            if not user_id:
                return {}
            
            response = self.client.table('user_goals').select('*').eq('user_id', user_id).execute()
            if response.data:
                return response.data[0]['goals']
            return {}
        except Exception as e:
            st.error(f"Failed to get goals: {str(e)}")
            return {}
    
    def get_user_stats(self) -> Dict[str, int]:
        """Get user statistics for admin (requires service role)."""
        try:
            # This would need service role key for admin functions
            # For now, return mock data
            return {
                'total_users': 1,
                'active_users': 1,
                'demo_users': 0
            }
        except Exception as e:
            st.error(f"Failed to get stats: {str(e)}")
            return {'total_users': 0, 'active_users': 0, 'demo_users': 0}

# Global instance
@st.cache_resource
def get_supabase_auth():
    """Get cached Supabase auth instance."""
    return SupabaseAuth()

# Helper functions for compatibility
def get_current_user():
    """Get current user email."""
    auth = get_supabase_auth()
    return auth.get_current_user()

def is_authenticated():
    """Check if user is authenticated."""
    return st.session_state.get('authenticated', False)
