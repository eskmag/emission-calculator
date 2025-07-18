import streamlit as st
from main.utils.supabase_auth import get_current_user, is_authenticated

st.set_page_config(
    page_title="Carbon Emissions Calculator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Personalized greeting
if is_authenticated():
    username = get_current_user()
    st.title(f"🌍 Welcome back, {username}!")
    st.markdown(f"""
        Welcome to your **Carbon Emissions Calculator!** 
        Track your **monthly carbon footprint** and work towards your sustainability goals.
    """)
else:
    st.title("🌍 Carbon Emissions Calculator")
    st.markdown("""
        Welcome to the **Carbon Emissions Calculator!** 
        This tool helps you estimate your **monthly carbon footprint** based on your transportation, energy usage, and food consumption.
    """)

st.divider()

# Quick navigation section
st.markdown("### 🚀 Quick Start")
st.markdown("Click on any section below to start calculating your carbon emissions:")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("categories/transport.py", label="🚗 **Transport**", help="Calculate emissions from cars, buses, trains, and flights")
    st.markdown("*Cars, buses, trains, flights*")

with col2:
    st.page_link("categories/energy.py", label="⚡ **Energy**", help="Calculate emissions from electricity, gas, and other home energy")
    st.markdown("*Electricity, gas, heating*")

with col3:
    st.page_link("categories/enhanced_food.py", label="🥗 **Food**", help="Calculate emissions from your diet and food choices")
    st.markdown("*Diet, meat, dairy, plant-based*")

st.divider()

# Personalized dashboard for authenticated users
if is_authenticated():
    # Show current emissions summary
    transport = st.session_state.get("transport_emissions", 0.0)
    energy = st.session_state.get("energy_emissions", 0.0)
    food = st.session_state.get("food_emissions", 0.0)
    total = transport + energy + food
    
    if total > 0:
        st.markdown("### 📊 Your Current Emissions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🚗 Transport", f"{transport:.1f} kg CO₂")
        with col2:
            st.metric("⚡ Energy", f"{energy:.1f} kg CO₂")
        with col3:
            st.metric("🥗 Food", f"{food:.1f} kg CO₂")
        with col4:
            st.metric("📊 Total", f"{total:.1f} kg CO₂")
        
        # Show progress towards goals
        if 'carbon_goals' in st.session_state:
            monthly_target = st.session_state['carbon_goals']['monthly_target']
            progress = (total / monthly_target) * 100 if monthly_target > 0 else 0
            
            st.markdown("### 🎯 Goal Progress")
            st.progress(min(progress / 100, 1.0))
            
            if progress <= 100:
                st.success(f"Great job! You're at {progress:.1f}% of your monthly target ({monthly_target:.1f} kg CO₂).")
            else:
                st.warning(f"You're at {progress:.1f}% of your monthly target ({monthly_target:.1f} kg CO₂). Consider ways to reduce emissions.")
        
        st.divider()
    else:
        st.info("📝 Complete the emission calculators to see your personalized dashboard here.")
        st.divider()

st.markdown("""
    ### 📊 How It Works
    
    Your carbon emissions are calculated based on your **monthly activities** across three main categories:
    
    1. **🚗 Transport Emissions**: Enter your monthly travel details for cars, buses, trains, and flights
    2. **⚡ Energy Emissions**: Input your monthly energy consumption data for electricity, gas, and other sources
    3. **🥗 Food Emissions**: Select your diet type or provide detailed food consumption data
    4. **📈 Results & Analytics**: View your total emissions, comparisons, and personalized recommendations
    5. **🎯 Goals & Progress**: Set reduction targets and track your progress over time
""")

st.divider()

st.markdown("""
    ### 🌱 Why Calculate Your Carbon Emissions?
    
    Understanding your carbon footprint is the first step towards reducing it. By identifying the areas where you can make changes, you can contribute to a more sustainable future.
    
    **🌍 Your actions matter!** Every small change can lead to a significant impact on our planet.
""")

# Add some key statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌍 Global Average", "833 kg CO₂", "per month")
    st.caption("Average monthly emissions worldwide")

with col2:
    st.metric("🇪🇺 EU Average", "667 kg CO₂", "per month")
    st.caption("Average monthly emissions in Europe")

with col3:
    st.metric("🎯 Paris Agreement Target", "167 kg CO₂", "per month")
    st.caption("Target to limit global warming to 1.5°C")

st.divider()

st.markdown("""
    ### 📚 Learn More
    
    **Climate Change Resources:**
    - [UN Sustainable Development Goal #13](https://sdgs.un.org/goals/goal13)
    - [The Intergovernmental Panel on Climate Change (IPCC)](https://www.ipcc.ch/)
    - [World Health Organization (WHO) - Climate Change](https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health)
    - [United Nations Environment Programme (UNEP)](https://www.unep.org/)
    
    **Ready to get started?** Use the navigation menu on the left or the quick start buttons above! 🚀
""")


