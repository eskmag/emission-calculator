import streamlit as st
from main.core.energy import energy_emissions
st.set_page_config(
    page_title="Energy Emissions",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Energy Emissions Calculator")
st.markdown("""
    Welcome to the **Energy Emissions Calculator!**
    This tool helps you estimate your carbon footprint based on your energy consumption, including electricity, gas, and other sources.
            
    ### How to Use:
    1. **Select your household energy sources**: Choose from electricity, oil, gas, wood, or other sources.
    2. **Input your energy consumption**: Enter the amount of energy consumed in kilowatt-hours (kWh) for each selected source.
    3. **Calculate your emissions**: Click the "Calculate Energy Emissions" button to see your total energy emissions in kilograms of CO2.
""")

st.divider()

energy_sources = st.multiselect(
    "Select your household energy sources:",
    options=["Electricity", "Oil", "Gas", "Wood", "Other"]
)

energy_inputs = {}

if "Electricity" in energy_sources:
    energy_inputs["kwh_electricity"] = st.number_input("Electricity (kWh):", min_value=0, value=0)

if "Oil" in energy_sources:
    energy_inputs["kwh_oil"] = st.number_input("Oil (kWh):", min_value=0, value=0)

if "Gas" in energy_sources:
    energy_inputs["kwh_gas"] = st.number_input("Gas (kWh):", min_value=0, value=0)

if "Wood" in energy_sources:
    energy_inputs["kwh_wood"] = st.number_input("Wood (kWh):", min_value=0, value=0)

total_energy_emissions = energy_emissions(**energy_inputs)

if st.button("Calculate Energy Emissions"):
    st.subheader("Total Energy Emissions")
    st.write(f"Your total energy emissions are: **{total_energy_emissions:.2f} kg CO2**")
    
    st.markdown("""
        ### Tips to Reduce Energy Emissions:
        - Use energy-efficient appliances.
        - Switch to renewable energy sources.
        - Insulate your home to reduce heating needs.
        - Consider using a programmable thermostat.
    """)