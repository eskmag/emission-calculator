import streamlit as st
from main.core.energy import energy_emissions
from main.utils.validators import validate_and_show_warning, validate_energy_input
from main.utils.supabase_auth import get_supabase_auth, get_current_user, is_authenticated
st.set_page_config(
    page_title="Energy Emissions",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Energy Emissions Calculator")
st.markdown("""
    Welcome to the **Energy Emissions Calculator!**
    This tool helps you estimate your **monthly carbon footprint** based on your energy consumption, including electricity, gas, and other sources.
            
    ### How to Use:
    1. **Select your household energy sources**: Choose from electricity, oil, gas, wood, or other sources.
    2. **Input your energy consumption**: Enter the amount of energy consumed in kilowatt-hours (kWh) **per month** for each selected source.
    3. **Calculate your emissions**: Click the "Calculate Energy Emissions" button to see your total monthly energy emissions in kilograms of CO2.
""")

st.divider()

energy_sources = st.multiselect(
    "Select your household energy sources:",
    options=["Electricity", "Oil", "Gas", "Wood"]
)

energy_inputs = {}

if energy_sources:
    st.subheader("Enter monthly energy consumption (kWh)")
    cols = st.columns(len(energy_sources))

    for i, source in enumerate(energy_sources):
        label = f"{source} (kWh per month):"
        key = f"kwh_{source.lower()}"
        energy_inputs[key] = cols[i].number_input(label, min_value=0, value=0, help=f"Monthly {source.lower()} consumption")

if st.button("Calculate Energy Emissions"):
    # Validate inputs before calculation
    validation_errors = []
    
    # Validate energy inputs
    for key, value in energy_inputs.items():
        source_name = key.replace("kwh_", "").title()
        if not validate_and_show_warning(value, validate_energy_input, f"{source_name} consumption", st):
            validation_errors.append(source_name.lower())
    
    if validation_errors:
        st.error(f"Please check your input for: {', '.join(validation_errors)}")
    else:
        try:
            total_energy_emissions = energy_emissions(
                kwh_electricity=energy_inputs.get("kwh_electricity", 0),
                kwh_oil=energy_inputs.get("kwh_oil", 0),
                kwh_gas=energy_inputs.get("kwh_gas", 0),
                kwh_wood=energy_inputs.get("kwh_wood", 0)   
            )

            st.subheader("Total Monthly Energy Emissions")
            st.write(f"Your total monthly energy emissions are: **{total_energy_emissions:.2f} kg CO2**")
            
            # Store in session state for use in other pages
            st.session_state["energy_emissions"] = total_energy_emissions
            
            # Save to database if user is authenticated
            if is_authenticated():
                auth = get_supabase_auth()
                emission_details = {
                    'kwh_electricity': energy_inputs.get("kwh_electricity", 0),
                    'kwh_oil': energy_inputs.get("kwh_oil", 0),
                    'kwh_gas': energy_inputs.get("kwh_gas", 0),
                    'kwh_wood': energy_inputs.get("kwh_wood", 0),
                    'calculation_date': str(st.session_state.get('calculation_date', ''))
                }
                
                if auth.save_user_emissions('energy', total_energy_emissions, emission_details):
                    st.success("✅ Energy emissions saved to your profile!")
                else:
                    st.warning("Could not save energy emissions to database.")
            
            st.markdown("""
                ### Tips to Reduce Energy Emissions:
                - Use energy-efficient appliances.
                - Switch to renewable energy sources.
                - Insulate your home to reduce heating needs.
                - Consider using a programmable thermostat.
            """)
            
        except Exception as e:
            st.error(f"Error calculating energy emissions: {str(e)}")
            st.info("Please check your inputs and try again.")
else:
    st.warning("Please select your energy sources and enter your consumption to calculate emissions.")