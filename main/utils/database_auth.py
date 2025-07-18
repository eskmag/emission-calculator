"""
Database-based authentication system for the emission calculator.
Uses SQLite for secure, reliable user management.
"""

import streamlit as st
import sqlite3
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from pathlib import Path

class DatabaseAuth:
    """Database-based authentication system using SQLite."""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    is_admin BOOLEAN DEFAULT 0,
                    settings TEXT DEFAULT '{}'
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_token TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_emissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date DATE,
                    transport_emissions REAL DEFAULT 0,
                    energy_emissions REAL DEFAULT 0,
                    food_emissions REAL DEFAULT 0,
                    total_emissions REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    annual_target REAL,
                    monthly_target REAL,
                    start_date DATE,
                    target_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            conn.commit()
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt using SHA-256."""
        salt = "emission_calculator_salt_2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str = "") -> bool:
        """Register a new user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if user already exists
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    return False
                
                # Create new user
                password_hash = self._hash_password(password)
                cursor.execute("""
                    INSERT INTO users (username, password_hash, email, settings)
                    VALUES (?, ?, ?, ?)
                """, (username, password_hash, email, json.dumps({
                    "units": "metric",
                    "language": "en",
                    "notifications": True
                })))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user by username
                cursor.execute("""
                    SELECT id, password_hash, is_active 
                    FROM users 
                    WHERE username = ?
                """, (username,))
                
                user = cursor.fetchone()
                if not user:
                    return False
                
                user_id, stored_hash, is_active = user
                
                # Check if user is active
                if not is_active:
                    return False
                
                # Verify password
                password_hash = self._hash_password(password)
                if stored_hash == password_hash:
                    # Update last login
                    cursor.execute("""
                        UPDATE users 
                        SET last_login = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (user_id,))
                    conn.commit()
                    return True
                
                return False
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, username, email, created_at, last_login, 
                           is_active, is_admin, settings
                    FROM users 
                    WHERE username = ?
                """, (username,))
                
                user = cursor.fetchone()
                if not user:
                    return None
                
                user_id, username, email, created_at, last_login, is_active, is_admin, settings = user
                
                return {
                    "id": user_id,
                    "username": username,
                    "email": email or "",
                    "created_at": created_at,
                    "last_login": last_login,
                    "is_active": is_active,
                    "is_admin": is_admin,
                    "settings": json.loads(settings) if settings else {}
                }
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def update_user_settings(self, username: str, settings: Dict) -> bool:
        """Update user settings."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get current settings
                cursor.execute("SELECT settings FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                if not result:
                    return False
                
                current_settings = json.loads(result[0]) if result[0] else {}
                current_settings.update(settings)
                
                # Update settings
                cursor.execute("""
                    UPDATE users 
                    SET settings = ? 
                    WHERE username = ?
                """, (json.dumps(current_settings), username))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def save_user_emissions(self, username: str, transport: float, energy: float, food: float) -> bool:
        """Save user emissions data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user ID
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user = cursor.fetchone()
                if not user:
                    return False
                
                user_id = user[0]
                total = transport + energy + food
                today = datetime.now().date()
                
                # Insert or update today's emissions
                cursor.execute("""
                    INSERT OR REPLACE INTO user_emissions 
                    (user_id, date, transport_emissions, energy_emissions, food_emissions, total_emissions)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, today, transport, energy, food, total))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_user_emissions(self, username: str, days: int = 30) -> List[Dict]:
        """Get user emissions history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user ID
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user = cursor.fetchone()
                if not user:
                    return []
                
                user_id = user[0]
                
                # Get emissions data
                cursor.execute("""
                    SELECT date, transport_emissions, energy_emissions, food_emissions, total_emissions
                    FROM user_emissions 
                    WHERE user_id = ? AND date >= date('now', '-{} days')
                    ORDER BY date DESC
                """.format(days), (user_id,))
                
                emissions = []
                for row in cursor.fetchall():
                    emissions.append({
                        "date": row[0],
                        "transport": row[1],
                        "energy": row[2],
                        "food": row[3],
                        "total": row[4]
                    })
                
                return emissions
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    def save_user_goals(self, username: str, annual_target: float, monthly_target: float) -> bool:
        """Save or update user goals."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user ID
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user = cursor.fetchone()
                if not user:
                    return False
                
                user_id = user[0]
                
                # Insert or update goals
                cursor.execute("""
                    INSERT OR REPLACE INTO user_goals 
                    (user_id, annual_target, monthly_target, start_date, target_date, updated_at)
                    VALUES (?, ?, ?, date('now'), date('now', '+1 year'), CURRENT_TIMESTAMP)
                """, (user_id, annual_target, monthly_target))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_user_goals(self, username: str) -> Optional[Dict]:
        """Get user goals."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user ID
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user = cursor.fetchone()
                if not user:
                    return None
                
                user_id = user[0]
                
                # Get goals
                cursor.execute("""
                    SELECT annual_target, monthly_target, start_date, target_date
                    FROM user_goals 
                    WHERE user_id = ?
                    ORDER BY updated_at DESC
                    LIMIT 1
                """, (user_id,))
                
                goal = cursor.fetchone()
                if not goal:
                    return None
                
                return {
                    "annual_target": goal[0],
                    "monthly_target": goal[1],
                    "start_date": goal[2],
                    "target_date": goal[3]
                }
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def get_user_stats(self) -> Dict:
        """Get user statistics for admin."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total users
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]
                
                # Active users (logged in within last 30 days)
                cursor.execute("""
                    SELECT COUNT(*) FROM users 
                    WHERE last_login >= date('now', '-30 days')
                """)
                active_users = cursor.fetchone()[0]
                
                # Demo users
                cursor.execute("SELECT COUNT(*) FROM users WHERE username LIKE 'demo_%'")
                demo_users = cursor.fetchone()[0]
                
                return {
                    "total_users": total_users,
                    "active_users": active_users,
                    "demo_users": demo_users
                }
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"total_users": 0, "active_users": 0, "demo_users": 0}
    
    def cleanup_demo_users(self, days_old: int = 1) -> int:
        """Remove demo users older than specified days."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete old demo users
                cursor.execute("""
                    DELETE FROM users 
                    WHERE username LIKE 'demo_%' 
                    AND created_at < date('now', '-{} days')
                """.format(days_old))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                return deleted_count
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0

# Updated Streamlit authentication functions
def init_auth_session():
    """Initialize authentication session state."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'auth_system' not in st.session_state:
        st.session_state.auth_system = DatabaseAuth()

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
                if auth.register_user(username, password, email):
                    st.success("Registration successful! You can now login.")
                    st.balloons()
                else:
                    st.error("Username already exists or registration failed")

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
        st.markdown("- Secure data storage")

def get_current_user() -> Optional[str]:
    """Get current authenticated user."""
    return st.session_state.get('username')

def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get('authenticated', False)
