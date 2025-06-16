import streamlit as st


home = st.Page(
    "overview/home.py", title="Home", icon="🏠", default=True,
)

transport = st.Page(
    "categories/transport.py", title="Transport", icon="🚗",
)
energy = st.Page(
    "categories/energy.py", title="Energy", icon="⚡",
)
food = st.Page(
    "categories/diet.py", title="Diet", icon="🥗",
)

total = st.Page(
    "results/total.py", title="Total Emissions", icon="🌍",
)

pg = st.navigation(
    {
        "Overview": [home],
        "Categories": [transport, energy, food],
        "Results": [total],
    }
)

pg.run()