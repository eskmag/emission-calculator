import streamlit as st
from main.utils.supabase_auth import get_current_user, is_authenticated, get_supabase_auth
from datetime import datetime

if not is_authenticated():
    st.warning("Please login to access your profile.")
    st.stop()

st.set_page_config(
    page_title="User Profile",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("👤 User Profile")

username = get_current_user()
auth = get_supabase_auth()

if username:
    st.markdown(f"### Welcome, **{username}**!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Account Information")
        st.info(f"**Email:** {username}")
        st.info(f"**Member since:** {datetime.now().strftime('%B %d, %Y')}")
    
    with col2:
        st.subheader("⚙️ Settings")
        
        with st.form("settings_form"):
            units = st.selectbox(
                "Units",
                ["metric", "imperial"],
                index=0
            )
            
            language = st.selectbox(
                "Language",
                ["en", "es", "fr", "de"],
                index=0  # Default to English
            )
            
            notifications = st.checkbox(
                "Enable notifications",
                value=True
            )
            
            submit = st.form_submit_button("Update Settings")
            
            if submit:
                new_settings = {
                    'units': units,
                    'language': language,
                    'notifications': notifications
                }
                
                if auth.update_user_settings(username, new_settings):
                    st.success("Settings updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update settings.")
    
    st.divider()
    
    # Emission Summary
    st.subheader("📈 Your Carbon Footprint Summary")
    
    # Get current emissions from session
    transport = st.session_state.get("transport_emissions", 0.0)
    energy = st.session_state.get("energy_emissions", 0.0)
    food = st.session_state.get("food_emissions", 0.0)
    total = transport + energy + food
    
    if total > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Transport", f"{transport:.1f} kg CO₂")
        with col2:
            st.metric("Energy", f"{energy:.1f} kg CO₂")
        with col3:
            st.metric("Food", f"{food:.1f} kg CO₂")
        with col4:
            st.metric("Total", f"{total:.1f} kg CO₂")
        
        # Show progress towards goals
        if 'carbon_goals' in st.session_state:
            monthly_target = st.session_state['carbon_goals']['monthly_target']
            progress = (total / monthly_target) * 100 if monthly_target > 0 else 0
            
            st.subheader("🎯 Goal Progress")
            st.progress(min(progress / 100, 1.0))
            
            if progress <= 100:
                st.success(f"Great job! You're at {progress:.1f}% of your monthly target.")
            else:
                st.warning(f"You're at {progress:.1f}% of your monthly target. Consider ways to reduce emissions.")
    else:
        st.info("Complete the emission calculators to see your carbon footprint summary here.")
    
    st.divider()
    
    # Account Actions
    st.subheader("🔧 Account Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset All Data", type="secondary"):
            # Clear all emission data
            keys_to_clear = [
                'transport_emissions', 'energy_emissions', 'food_emissions',
                'carbon_goals', 'progress_data'
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("All data has been reset!")
            st.rerun()
    
    with col2:
        st.markdown("**Export Data** (Coming Soon)")
        st.button("📁 Export Data", disabled=True, help="Feature coming soon")

else:
    st.error("Unable to load user information.")
