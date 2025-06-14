import streamlit as st

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
