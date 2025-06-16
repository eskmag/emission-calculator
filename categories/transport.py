import streamlit as st
from main.core.transport import transport_emissions

st.set_page_config(
    page_title="Transport Emissions",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Transport Emissions Calculator")
st.markdown("""
    Welcome to the **Transport Emissions Calculator!**
    This tool helps you estimate your **monthly carbon footprint** based on your transportation choices, including car, bus, train, and air travel.
            
    ### How to Use:
    1. **Car Emissions**: Enter the kilometers traveled by car and select the fuel type (Petrol, Diesel, Electric).
    2. **Bus Emissions**: Enter the kilometers traveled by bus and select the fuel type (Diesel, Electric, Biofuel).
    3. **Train Emissions**: Enter the kilometers traveled by train and select the train type (Electric, Diesel).
    4. **Air Travel Emissions**: Enter the number of short, medium, and long flights taken.
    5. **Calculate Transport Emissions**: Click the "Calculate Transport Emissions" button to see your total transport emissions in kilograms of CO2.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("Car Emissions")
    km_car = st.number_input("Enter kilometers traveled by car:", min_value=0, value=0)
    car_fuel_type = st.selectbox("Select car fuel type:", ["Petrol", "Diesel", "Electric"])

    st.header("Bus Emissions")
    km_bus = st.number_input("Enter kilometers traveled by bus:", min_value=0, value=0)
    bus_fuel_type = st.selectbox("Select bus fuel type:", ["Diesel", "Electric", "Biofuel"])

with col2:
    st.header("Train Emissions")
    km_train = st.number_input("Enter kilometers traveled by train:", min_value=0, value=0)
    train_type = st.selectbox("Select train fuel type:", ["Electric", "Diesel"])

    st.header("Air Travel Emissions")
    short_flights = st.number_input("Enter number of short flights (up to 500 km):", min_value=0, value=0)
    medium_flights = st.number_input("Enter number of medium flights (500-1500 km):", min_value=0, value=0)
    long_flights = st.number_input("Enter number of long flights (over 1500 km):", min_value=0, value=0)

if st.button("Calculate Transport Emissions"):
    total_transport_emissions = transport_emissions(
        km_car=km_car,
        car_fuel_type=car_fuel_type.lower(),
        km_bus=km_bus,
        bus_fuel_type=bus_fuel_type.lower(),
        km_train=km_train,
        train_type=train_type.lower(),
        short_flights=short_flights,
        medium_flights=medium_flights,
        long_flights=long_flights
    )

    total = total_transport_emissions

    st.subheader("Total Transport Emissions")
    st.write(f"Your total transport emissions are: **{total:.2f} kg CO2**")

    st.session_state["transport_emissions"] = total_transport_emissions