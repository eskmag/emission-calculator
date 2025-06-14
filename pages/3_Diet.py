import streamlit as st
from main.core.food import food_emissions

st.set_page_config(
    page_title="Food Emissions",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Food Emissions Calculator")
st.markdown("""
    Welcome to the **Food Emissions Calculator!**
    This tool helps you estimate your carbon footprint based on your diet, including meat, dairy, and plant-based foods.
    
    ### How to Use:
    1. **Select your diet type**: Choose from options like Vegan, Vegetarian, Omnivore, or Carnivore.
    2. **Input your food consumption**: Enter the amount of meat, dairy, and plant-based foods consumed in kilograms per week.
    3. **Calculate your emissions**: Click the "Calculate Food Emissions" button to see your total food emissions in kilograms of CO2.
""")

st.divider()