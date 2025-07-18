"""
Migration script to move data from SQLite to Supabase.
Run this after setting up your Supabase project.
"""

import sqlite3
import os
from supabase import create_client, Client
from datetime import datetime
import json
import hashlib
from dotenv import load_dotenv

def migrate_sqlite_to_supabase():
    """Migrate existing SQLite data to Supabase."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Supabase client
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')  # Use service role key for admin operations
    
    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase credentials. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables.")
    
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Connect to SQLite database
    if not os.path.exists('users.db'):
        print("No SQLite database found. Nothing to migrate.")
        return
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    print("Starting migration from SQLite to Supabase...")
    
    # Migrate users
    print("Migrating users...")
    cursor.execute("SELECT username, email, password_hash, created_at FROM users")
    users = cursor.fetchall()
    
    user_mapping = {}  # SQLite username -> Supabase user_id
    
    for username, email, password_hash, created_at in users:
        try:
            # Handle missing email - create one from username
            if not email or email.strip() == '':
                email = f"{username}@example.com"
            
            # Create user in Supabase Auth
            # Note: We can't migrate passwords directly, so we'll create users with temporary passwords
            # and they'll need to reset their passwords
            temp_password = hashlib.sha256(f"{username}_{email}".encode()).hexdigest()[:12]
            
            auth_response = supabase.auth.admin.create_user({
                "email": email,
                "password": temp_password,
                "email_confirm": True,
                "user_metadata": {
                    "username": username
                }
            })
            
            if auth_response.user:
                user_id = auth_response.user.id
                user_mapping[username] = user_id
                
                # Create user profile
                supabase.table('user_profiles').insert({
                    'user_id': user_id,
                    'username': username,
                    'email': email,
                    'created_at': created_at
                }).execute()
                
                print(f"✓ Migrated user: {username}")
            else:
                print(f"✗ Failed to migrate user: {username}")
                
        except Exception as e:
            print(f"✗ Error migrating user {username}: {str(e)}")
    
    # Migrate user goals
    print("Migrating user goals...")
    cursor.execute("""
        SELECT u.username, ug.annual_target, ug.monthly_target, ug.start_date, ug.target_date, ug.created_at, ug.updated_at
        FROM user_goals ug
        JOIN users u ON ug.user_id = u.id
    """)
    goals = cursor.fetchall()
    
    for username, annual_target, monthly_target, start_date, target_date, created_at, updated_at in goals:
        if username in user_mapping:
            try:
                user_id = user_mapping[username]
                goals_data = {
                    'annual_target': annual_target,
                    'monthly_target': monthly_target,
                    'start_date': start_date,
                    'target_date': target_date,
                    'created_at': created_at
                }
                
                supabase.table('user_goals').insert({
                    'user_id': user_id,
                    'goals': goals_data,
                    'updated_at': updated_at or datetime.now().isoformat()
                }).execute()
                
                print(f"✓ Migrated goals for: {username}")
            except Exception as e:
                print(f"✗ Error migrating goals for {username}: {str(e)}")
    
    # Migrate user emissions
    print("Migrating user emissions...")
    cursor.execute("""
        SELECT u.username, ue.date, ue.transport_emissions, ue.energy_emissions, ue.food_emissions, ue.total_emissions, ue.created_at
        FROM user_emissions ue
        JOIN users u ON ue.user_id = u.id
    """)
    emissions = cursor.fetchall()
    
    for username, date, transport_emissions, energy_emissions, food_emissions, total_emissions, created_at in emissions:
        if username in user_mapping:
            try:
                user_id = user_mapping[username]
                
                # Insert separate records for each emission category
                if transport_emissions and transport_emissions > 0:
                    supabase.table('user_emissions').insert({
                        'user_id': user_id,
                        'category': 'transport',
                        'emissions': transport_emissions,
                        'details': {'date': date, 'source': 'migration'},
                        'created_at': created_at
                    }).execute()
                
                if energy_emissions and energy_emissions > 0:
                    supabase.table('user_emissions').insert({
                        'user_id': user_id,
                        'category': 'energy',
                        'emissions': energy_emissions,
                        'details': {'date': date, 'source': 'migration'},
                        'created_at': created_at
                    }).execute()
                
                if food_emissions and food_emissions > 0:
                    supabase.table('user_emissions').insert({
                        'user_id': user_id,
                        'category': 'food',
                        'emissions': food_emissions,
                        'details': {'date': date, 'source': 'migration'},
                        'created_at': created_at
                    }).execute()
                
                print(f"✓ Migrated emissions for: {username}")
            except Exception as e:
                print(f"✗ Error migrating emissions for {username}: {str(e)}")
    
    conn.close()
    print("Migration completed!")
    print(f"Migrated {len(user_mapping)} users to Supabase.")
    print("Note: Users will need to reset their passwords as they couldn't be migrated directly.")

if __name__ == "__main__":
    migrate_sqlite_to_supabase()
