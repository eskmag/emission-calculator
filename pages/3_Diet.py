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

diet_type = st.selectbox(
    "Select your diet type:",
    options=[
        ("high_meat", "High Meat"), 
        ("average", "Average"), 
        ("vegetarian", "Vegetarian"), 
        ("vegan", "Vegan")
    ],
    format_func=lambda x: x[1] # Display the second element of the tuple
)

selected_key = diet_type[0]

if st.button("Calculate Food Emissions"):
    food_emissions_result = food_emissions(diet_type=selected_key)
    
    st.subheader("Total Food Emissions")
    st.write(f"Your total food emissions are: **{food_emissions_result:.2f} kg CO2**")
    
    st.markdown("""
        ### Tips to Reduce Food Emissions:
        - Reduce meat and dairy consumption.
        - Choose local and seasonal produce.
        - Minimize food waste.
        - Opt for plant-based alternatives.
    """)    

    st.session_state["food_emissions"] = food_emissions_result

