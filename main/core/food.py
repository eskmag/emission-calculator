from main.data.emission_factors import FOOD_FACTORS

def food_emissions(diet_type: str) -> float:
    """
    Calculate food emissions based on diet type.
    
    :param diet_type: Type of diet ('high_meat', 'average', 'vegetarian', 'vegan').
    :return: Monthly CO2 emissions in kg.
    """
    daily_emission = FOOD_FACTORS.get(diet_type, FOOD_FACTORS['average'])  # Default to 'average' if diet type is unknown
    return daily_emission * 30  # Monthly emissions