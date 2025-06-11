

def energy_emissions(**kwargs) -> float:
    from main.data.emission_factors import ENERGY_FACTORS

    total = 0.0
    for source, kwh in kwargs.items():
        factor = ENERGY_FACTORS.get(source, 0)
        total += kwh * factor
    return total