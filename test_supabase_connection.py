"""
Test script to verify Supabase connection and setup.
Run this after creating your Supabase project and setting up .env file.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

def test_supabase_connection():
    """Test Supabase connection and basic operations."""
    
    # Load environment variables
    load_dotenv()
    
    # Get Supabase credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Missing Supabase credentials!")
        print("Please create a .env file with:")
        print("SUPABASE_URL=your-project-url")
        print("SUPABASE_ANON_KEY=your-anon-key")
        return False
    
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully!")
        
        # Test basic connection (this will fail if tables don't exist yet)
        try:
            response = supabase.table('user_profiles').select('*').limit(1).execute()
            print("✅ Database connection successful!")
            print(f"✅ Found {len(response.data)} records in user_profiles table")
        except Exception as e:
            print("⚠️  Database tables not set up yet (this is expected for new projects)")
            print(f"Error: {str(e)}")
            print("You'll need to create the database schema first.")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Supabase connection...")
    success = test_supabase_connection()
    
    if success:
        print("\n🎉 Supabase setup looks good!")
        print("Next steps:")
        print("1. Create the database schema in Supabase dashboard")
        print("2. Run the migration script to move data")
        print("3. Update your Streamlit app to use Supabase auth")
    else:
        print("\n❌ Supabase setup needs attention.")
        print("Check your .env file and Supabase project settings.")
