from emission_calculator.calculator import calculate_transport_emissions, calculate_energy_emissions, calculate_food_emissions


def get_float_input(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_diet_type() -> str:
    print("\nSelect your diet type:")
    print("1. High Meat")
    print("2. Average")
    print("3. Vegetarian")
    print("4. Vegan")

    choices = {
        '1': 'high_meat',
        '2': 'average',
        '3': 'vegetarian',
        '4': 'vegan'
    }

    while True:
        choice = input("Enter the number corresponding to your diet type: ")
        if choice in choices:
            return choices[choice]
        else:
            print("Invalid choice. Please select a valid diet type.")


def run_cli():
    print("Wlecome to the Emission Calculator")
    print("Let's calculate your emissions based on transport, food, and energy usage.\n")

    # Transport Emissions
    km_car = get_float_input("How many KM do you drive per month by car? ")
    km_bus = get_float_input("How many KM do you travel by bus per month? ")
    km_plane = get_float_input("How many KM do you travel by plane per month? ")
    transport_emission = calculate_transport_emissions(km_car, km_bus, km_plane)
   
    # Food Emissions
    diet_type = get_diet_type()
    diet_emission = calculate_food_emissions(diet_type)

    # Energy Emissions
    print("\nEnergy usage per month (in kWh):")
    kwh_electricity = get_float_input("Electricity: ")
    kwh_oil = get_float_input("Oil: ")
    kwh_gas = get_float_input("Gas: ")
    kwh_wood = get_float_input("Wood: ")
    energy_emission = calculate_energy_emissions(kwh_electricity, kwh_oil, kwh_gas, kwh_wood)

    # Total Emissions
    total_emission = transport_emission + diet_emission + energy_emission
    print("\n--- Emission Summary ---")
    print(f"Transport Emissions: {transport_emission:.2f} kg CO2")
    print(f"Food Emissions: {diet_emission:.2f} kg CO2")
    print(f"Energy Emissions: {energy_emission:.2f} kg CO2")
    print(f"Total Monthly Emissions: {total_emission:.2f} kg CO2\n")


if __name__ == "__main__":
    run_cli()