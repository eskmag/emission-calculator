def calulate_transport_emissions(km_car: float, km_bus: float, km_flight: float) -> float:
    CO2_CAR = 0.192 # kg CO2 per km
    CO2_BUS = 0.105
    CO2_FLIGHT = 0.255
    emission_car = km_car * CO2_CAR
    emission_bus = km_bus * CO2_BUS
    emission_flight = km_flight * CO2_FLIGHT
    total_emission = emission_car + emission_bus + emission_flight
    return total_emission

