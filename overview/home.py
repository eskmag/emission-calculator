import streamlit as st
from main.core.transport import transport_emissions
from main.core.energy import energy_emissions
from main.core.food import food_emissions

st.set_page_config(
    page_title="Carbon Emissions Calculator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌍 Carbon Emissions Calculator")
st.markdown("""
    Welcome to the ***Carbon Emissions Calculator!*** 
    This tool helps you estimate your carbon footprint based on your *transportation*, *energy usage*, and *food consumption*.
    
    ⬅️ **You can easily navigate through the different sections using the sidebar.**
    Each section allows you to input your data, and the calculator will provide you with an estimate of your carbon emissions in kilograms of CO2.
""")

st.divider()

st.markdown("""
    ###### Your carbon emissions are based on your monthly activities, including transportation, energy consumption, and food choices.  
    
    ### How to Use:
    1. **Transport Emissions**: Enter your travel details for car, bus, train, and flights.
    2. **Energy Emissions**: Input your energy consumption data for electricity, gas, and other sources.
    3. **Food Emissions**: Provide details about your diet, including meat, dairy, and plant-based foods.
    4. **Results**: After entering your data, click the "Calculate" button to see your total carbon emissions.
""")

st.divider()
st.markdown("""
    ### Why Calculate Your Carbon Emissions?
    Understanding your carbon footprint is the first step towards reducing it. 
    By identifying the areas where you can make changes, you can contribute to a more sustainable future.
    
    🌍 **Your actions matter!** Every small change can lead to a significant impact on our planet.
    ### Resources for Further Reading:
    - [UN Sustatinble Devolopment Goal Nr. 13](https://sdgs.un.org/goals/goal13)
    - [The Intergovernmental Panel on Climate Change (IPCC)](https://www.ipcc.ch/)
    - [World Health Organization (WHO)](https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health)
    - [United Nations Environment Programme (UNEP)](https://www.unep.org/)
    
    🌱 **Let's get started!**
""")


