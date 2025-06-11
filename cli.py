from main.core.transport import transport_emissions
from main.core.food import food_emissions
from main.core.energy import energy_emissions
from main.utils.input_helpers import get_float_input, get_int_input, get_choice_input


def get_diet_type() -> str:
    choices = {
        '1': 'high_meat',
        '2': 'average',
        '3': 'vegetarian',
        '4': 'vegan'
    }
    return get_choice_input("\nSelect your diet type:", choices)


def get_fuel_type(vehicle: str, options: list[str]) -> str:
    choices = {str(i + 1): opt for i, opt in enumerate(options)}
    return get_choice_input(f"\nSelect {vehicle} fuel type:", choices)


def run_cli():
    print("Welcome to the Emission Calculator")
    print("Let's calculate your emissions based on transport, food, and energy usage.\n")

    # Transport Emissions
    km_car = get_float_input("How many KM do you drive by car per month? ")
    car_fuel_type = get_fuel_type("car", ["gasoline", "diesel"])

    km_bus = get_float_input("How many KM do you travel by bus per month? ")
    bus_fuel_type = get_fuel_type("bus", ["diesel", "biofuel", "electric"])

    km_train = get_float_input("How many KM do you travel by train per month? ")
    train_type = get_fuel_type("train", ["diesel", "electric"])

    print("\nEnter number of flights per month:")
    short_flights = int(get_int_input("Short flights (< 3h): "))
    medium_flights = int(get_int_input("Medium flights (3-6h): "))
    long_flights = int(get_int_input("Long flights (> 6h): "))

    transport_emission = transport_emissions(
        km_car, car_fuel_type,
        km_bus, bus_fuel_type,
        km_train, train_type,
        short_flights, medium_flights, long_flights
    )

    # Food Emissions
    diet_type = get_diet_type()
    diet_emission = food_emissions(diet_type)

    # Energy Emissions
    print("\nEnergy usage per month (in kWh):")
    kwh_electricity = get_float_input("Electricity: ")
    kwh_oil = get_float_input("Oil: ")
    kwh_gas = get_float_input("Gas: ")
    kwh_wood = get_float_input("Wood: ")
    energy_emission = energy_emissions(
        electricity=kwh_electricity,
        oil=kwh_oil,
        gas=kwh_gas,
        wood=kwh_wood
    )

    # Total Emissions
    total_emission = transport_emission + diet_emission + energy_emission
    print("\n--- Emission Summary ---")
    print(f"Transport Emissions: {transport_emission:.2f} kg CO2")
    print(f"Food Emissions: {diet_emission:.2f} kg CO2e")
    print(f"Energy Emissions: {energy_emission:.2f} kg CO2")
    print(f"Total Monthly Emissions: {total_emission:.2f} kg CO2\n")

if __name__ == "__main__":
    run_cli()