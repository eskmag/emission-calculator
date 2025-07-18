import streamlit as st
from main.core.transport import transport_emissions
from main.utils.validators import validate_and_show_warning, validate_km_input, validate_flights_input
from main.utils.supabase_auth import get_supabase_auth, get_current_user, is_authenticated

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
    1. **Car Emissions**: Enter the kilometers traveled by car **per month** and select the fuel type (Petrol, Diesel, Electric).
    2. **Bus Emissions**: Enter the kilometers traveled by bus **per month** and select the fuel type (Diesel, Electric, Biofuel).
    3. **Train Emissions**: Enter the kilometers traveled by train **per month** and select the train type (Electric, Diesel).
    4. **Air Travel Emissions**: Enter the number of short, medium, and long flights taken **per month** (average monthly flights).
    5. **Calculate Transport Emissions**: Click the "Calculate Transport Emissions" button to see your total monthly transport emissions in kilograms of CO2.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("Car Emissions")
    km_car = st.number_input("Enter kilometers traveled by car per month:", min_value=0, value=0, help="Monthly distance driven")
    car_fuel_type = st.selectbox("Select car fuel type:", ["Petrol", "Diesel", "Electric"])

    st.header("Bus Emissions")
    km_bus = st.number_input("Enter kilometers traveled by bus per month:", min_value=0, value=0, help="Monthly distance by bus")
    bus_fuel_type = st.selectbox("Select bus fuel type:", ["Diesel", "Electric", "Biofuel"])

with col2:
    st.header("Train Emissions")
    km_train = st.number_input("Enter kilometers traveled by train per month:", min_value=0, value=0, help="Monthly distance by train")
    train_type = st.selectbox("Select train fuel type:", ["Electric", "Diesel"])

    st.header("Air Travel Emissions")
    short_flights = st.number_input("Enter number of short flights per month (up to 500 km):", min_value=0.0, value=0.0, step=0.1, help="Average monthly short flights")
    medium_flights = st.number_input("Enter number of medium flights per month (500-1500 km):", min_value=0.0, value=0.0, step=0.1, help="Average monthly medium flights")
    long_flights = st.number_input("Enter number of long flights per month (over 1500 km):", min_value=0.0, value=0.0, step=0.1, help="Average monthly long flights")

if st.button("Calculate Transport Emissions"):
    # Validate inputs before calculation
    validation_errors = []
    
    # Validate distance inputs
    if not validate_and_show_warning(km_car, validate_km_input, "Car distance", st):
        validation_errors.append("car distance")
    if not validate_and_show_warning(km_bus, validate_km_input, "Bus distance", st):
        validation_errors.append("bus distance")
    if not validate_and_show_warning(km_train, validate_km_input, "Train distance", st):
        validation_errors.append("train distance")
    
    # Validate flight inputs
    if not validate_and_show_warning(short_flights, validate_flights_input, "Short flights", st):
        validation_errors.append("short flights")
    if not validate_and_show_warning(medium_flights, validate_flights_input, "Medium flights", st):
        validation_errors.append("medium flights")
    if not validate_and_show_warning(long_flights, validate_flights_input, "Long flights", st):
        validation_errors.append("long flights")
    
    if validation_errors:
        st.error(f"Please check your input for: {', '.join(validation_errors)}")
    else:
        try:
            transport_result = transport_emissions(
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

            total = transport_result['total'] if isinstance(transport_result, dict) else transport_result

            st.subheader("Total Monthly Transport Emissions")
            st.write(f"Your total monthly transport emissions are: **{total:.2f} kg CO2**")
            
            # Store in session state for use in other pages
            st.session_state["transport_emissions"] = total
            
            # Save to database if user is authenticated
            if is_authenticated():
                auth = get_supabase_auth()
                emission_details = {
                    'car_km': km_car,
                    'car_fuel': car_fuel_type,
                    'bus_km': km_bus,
                    'bus_fuel': bus_fuel_type,
                    'train_km': km_train,
                    'train_type': train_type,
                    'short_flights': short_flights,
                    'medium_flights': medium_flights,
                    'long_flights': long_flights,
                    'calculation_date': str(st.session_state.get('calculation_date', ''))
                }
                
                if auth.save_user_emissions('transport', total, emission_details):
                    st.success("✅ Transport emissions saved to your profile!")
                else:
                    st.warning("Could not save transport emissions to database.")
            
            # Show breakdown if available
            if isinstance(transport_result, dict) and 'breakdown' in transport_result:
                st.subheader("Emissions Breakdown")
                breakdown = transport_result['breakdown']
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Car", f"{breakdown['car']:.1f} kg CO2")
                with col2:
                    st.metric("Bus", f"{breakdown['bus']:.1f} kg CO2")
                with col3:
                    st.metric("Train", f"{breakdown['train']:.1f} kg CO2")
                with col4:
                    st.metric("Flights", f"{breakdown['flights']:.1f} kg CO2")
                    
        except Exception as e:
            st.error(f"Error calculating transport emissions: {str(e)}")
            st.info("Please check your inputs and try again.")

    st.session_state["transport_emissions"] = total