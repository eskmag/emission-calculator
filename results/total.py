import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Total Emissions",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Total Carbon Emissions")
st.markdown("""
    Here you can view your total carbon emissions calculated from all sections:
""")

st.page_link("categories/transport.py", label="### :green[Transport Emissions]", icon="🚗")
st.page_link("categories/energy.py", label="### :green[Energy Emissions]", icon="⚡")
st.page_link("categories/diet.py", label="### :green[Food Emissions]", icon="🥗")

st.divider()

# Hent verdier fra session_state
transport = st.session_state.get("transport_emissions", 0.0)
energy = st.session_state.get("energy_emissions", 0.0)
food = st.session_state.get("food_emissions", 0.0)

total_emissions = transport + energy + food

st.subheader("Total Carbon Emissions")
st.markdown(f"""
            Your total carbon emissions are: **{total_emissions:.2f} kg CO₂**
            
            ##### Breakdown by Category:
            - **Transport**: {transport:.2f} kg CO₂
            - **Energy**: {energy:.2f} kg CO₂
            - **Food**: {food:.2f} kg CO₂
            """)


emission_df = pd.DataFrame({
    "Emissions (kg CO₂)": [transport, energy, food]
}, index=["Transport", "Energy", "Food"])

st.subheader("Emissions Breakdown by Category")
st.bar_chart(emission_df, horizontal=True)