import yaml
from pathlib import Path


DATA_PATH = Path(__file__).parent / 'emission_factors.yaml'
# Load emission factors from the YAML file

with open(DATA_PATH, 'r') as file:
    emission_factors = yaml.safe_load(file)

TRANSPORT_FACTORS = emission_factors['transport']
FOOD_FACTORS = emission_factors['diet']
ENERGY_FACTORS = emission_factors['energy']

CAR_FUEL_CONSUMPTION = {
    'petrol': 0.2,  # L/km
    'diesel': 0.15,  # L/km
    'electric': 0.0   # kWh/km
}