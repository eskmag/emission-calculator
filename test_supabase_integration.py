"""
Test script to verify Supabase integration with the updated Streamlit app.
"""

import os
from dotenv import load_dotenv
from main.utils.supabase_auth import get_supabase_auth

def test_supabase_integration():
    """Test Supabase authentication integration."""
    
    print("🧪 Testing Supabase Integration...")
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize Supabase auth
        auth = get_supabase_auth()
        print("✅ Supabase auth initialized successfully")
        
        # Test user registration (with a test user)
        test_email = "test@example.com"
        test_password = "testpass123"
        test_username = "testuser"
        
        print(f"📝 Testing user registration with {test_email}...")
        
        # Note: This will fail if user already exists, which is expected
        registration_result = auth.register_user(test_email, test_password, test_username)
        
        if registration_result:
            print("✅ User registration successful")
        else:
            print("⚠️ User registration failed (might already exist)")
        
        # Test authentication
        print(f"🔐 Testing authentication...")
        auth_result = auth.authenticate(test_email, test_password)
        
        if auth_result:
            print("✅ Authentication successful")
            
            # Test saving emissions
            print("💾 Testing emissions saving...")
            emission_result = auth.save_user_emissions('transport', 10.5, {'test': 'data'})
            
            if emission_result:
                print("✅ Emissions saved successfully")
            else:
                print("❌ Failed to save emissions")
            
            # Test getting emissions
            print("📊 Testing emissions retrieval...")
            emissions = auth.get_user_emissions()
            print(f"✅ Retrieved {len(emissions)} emission records")
            
            # Test saving goals
            print("🎯 Testing goals saving...")
            test_goals = {'annual_target': 2000, 'monthly_target': 167}
            goals_result = auth.save_user_goals(test_goals)
            
            if goals_result:
                print("✅ Goals saved successfully")
            else:
                print("❌ Failed to save goals")
            
            # Test getting goals
            print("📈 Testing goals retrieval...")
            goals = auth.get_user_goals()
            print(f"✅ Retrieved goals: {goals}")
            
        else:
            print("❌ Authentication failed")
        
        print("\n🎉 Supabase integration test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_supabase_integration()
