import streamlit as st
import plotly.express as px

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

st.page_link("pages/1_Transport.py", label="### :green[Transport Emissions]", icon="🚗")
st.page_link("pages/2_Energy.py", label="### :green[Energy Emissions]", icon="⚡")
st.page_link("pages/3_Diet.py", label="### :green[Food Emissions]", icon="🥗")

st.divider()

transport = st.session_state.get("transport_emissions", 0.0)
energy = st.session_state.get("energy_emissions", 0.0)
food = st.session_state.get("food_emissions", 0.0)
total_emissions = transport + energy + food

st.subheader("Total Carbon Emissions")
st.write(f"Your total carbon emissions are: **{total_emissions:.2f} kg CO2**")

emission_data = {
    "Category": ["Transport", "Energy", "Food"],
    "Emissions (kg CO2)": [transport, energy, food]
}

fig = px.pie(
    emission_data,
    names="Category",
    values="Emissions (kg CO2)",
    title="Carbon Emissions Breakdown",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig, use_container_width=True)
