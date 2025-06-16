from main.data.emission_factors import TRANSPORT_FACTORS, CAR_FUEL_CONSUMPTION

def transport_emissions(km_car: float, car_fuel_type: str, km_bus: float, bus_fuel_type: str,
                        km_train: float, train_type: str, 
                        short_flights: int, medium_flights: int, long_flights: int) -> float:
    """
    Calculate transport emissions based on travel distance and fuel/type.

    :param km_car: Distance driven by car (in km).
    :param car_fuel_type: Fuel type used for car ('petrol', 'diesel').
    :param km_bus: Distance traveled by bus (in km).
    :param bus_fuel_type: Fuel type used for bus ('diesel', 'biofuel', 'electric').
    :param flight_distance_type: 'short', 'medium', or 'long' flight.
    :return: Total CO2 emissions in kg.
    """
    car_factor = TRANSPORT_FACTORS['car'].get(car_fuel_type, 0)
    car_consumption = CAR_FUEL_CONSUMPTION.get(car_fuel_type, 0)
    car_emission = km_car * car_factor * car_consumption

    bus_factor = TRANSPORT_FACTORS['bus'].get(bus_fuel_type, 0)
    train_factor = TRANSPORT_FACTORS['train'].get(train_type, 0)
    flight_factor = (
        TRANSPORT_FACTORS['flight']['short'] * short_flights +
        TRANSPORT_FACTORS['flight']['medium'] * medium_flights +
        TRANSPORT_FACTORS['flight']['long'] * long_flights
    )

    total_emission = (
        car_emission + 
        (km_bus * bus_factor) + 
        (km_train * train_factor) + 
        flight_factor
    )
    return total_emission