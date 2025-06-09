def calculate_transport_emissions(km_car: float, km_bus: float, km_flight: float) -> float:
    CO2_CAR = 0.192 # kg CO2 per km
    CO2_BUS = 0.105
    CO2_FLIGHT = 0.255
    emission_car = km_car * CO2_CAR
    emission_bus = km_bus * CO2_BUS
    emission_flight = km_flight * CO2_FLIGHT
    total_emission = emission_car + emission_bus + emission_flight
    return total_emission

def calulcate_food_emissions(diet_type: str) -> float:
    # CO2 emissions per kg of food consumed based on diet type
    CO2_DIET = {
        'high_meat': 7.2,
        'average': 5.6,
        'vegetarian': 3.8,
        'vegan': 2.9
    }
    daily = CO2_DIET.get(diet_type, 5.6)  # Default to 'average' if diet type is unknown
    return daily * 30 # Monthly emissions

def calculate_energy_emissions(kWh_used: float, energy_source: str) -> float:
    # CO2 emissions per kWh based on energy source
    CO2_PER_KWH = {
        'electricity': 0.02,  # kg CO2 per kWh
        'oil': 0.267,
        'wood': 0.018,
        'gas': 0.25
    }
    co2_factor = CO2_PER_KWH.get(energy_source, 0.02)  # Default to 'electricity' if source is unknown
    return kWh_used * co2_factor