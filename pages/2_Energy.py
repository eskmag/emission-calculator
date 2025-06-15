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
    options=["Electricity", "Oil", "Gas", "Wood"]
)

energy_inputs = {}

if energy_sources:
    st.subheader("Enter energy consumption (kWh)")
    cols = st.columns(len(energy_sources))

    for i, source in enumerate(energy_sources):
        label = f"{source} (kWh):"
        key = f"kwh_{source.lower()}"
        energy_inputs[key] = cols[i].number_input(label, min_value=0, value=0)

if st.button("Calculate Energy Emissions"):
    total_energy_emissions = energy_emissions(
        kwh_electricity=energy_inputs.get("kwh_electricity", 0),
        kwh_oil=energy_inputs.get("kwh_oil", 0),
        kwh_gas=energy_inputs.get("kwh_gas", 0),
        kwh_wood=energy_inputs.get("kwh_wood", 0)   
    )

    st.subheader("Total Energy Emissions")
    st.write(f"Your total energy emissions are: **{total_energy_emissions:.2f} kg CO2**")
    
    st.markdown("""
        ### Tips to Reduce Energy Emissions:
        - Use energy-efficient appliances.
        - Switch to renewable energy sources.
        - Insulate your home to reduce heating needs.
        - Consider using a programmable thermostat.
    """)

    st.session_state["energy_emissions"] = total_energy_emissions
else:
    st.warning("Please select your energy sources and enter your consumption to calculate emissions.")