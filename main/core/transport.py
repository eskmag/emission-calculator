from main.data.emission_factors import TRANSPORT_FACTORS, CAR_FUEL_CONSUMPTION
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def transport_emissions(km_car: float, car_fuel_type: str, km_bus: float, bus_fuel_type: str,
                        km_train: float, train_type: str, 
                        short_flights: float, medium_flights: float, long_flights: float) -> Dict[str, Any]:
    """
    Calculate monthly transport emissions based on travel distance and fuel/type.

    :param km_car: Monthly distance driven by car (in km).
    :param car_fuel_type: Fuel type used for car ('petrol', 'diesel', 'electric').
    :param km_bus: Monthly distance traveled by bus (in km).
    :param bus_fuel_type: Fuel type used for bus ('diesel', 'biofuel', 'electric').
    :param km_train: Monthly distance traveled by train (in km).
    :param train_type: Type of train ('electric', 'diesel').
    :param short_flights: Average monthly number of short flights.
    :param medium_flights: Average monthly number of medium flights.
    :param long_flights: Average monthly number of long flights.
    :return: Dict with total monthly emissions and breakdown by transport type.
    """
    try:
        # Car emissions calculation
        car_factor = TRANSPORT_FACTORS['car'].get(car_fuel_type, 0)
        car_consumption = CAR_FUEL_CONSUMPTION.get(car_fuel_type, 0)
        car_emission = km_car * car_factor * car_consumption

        # Bus emissions
        bus_factor = TRANSPORT_FACTORS['bus'].get(bus_fuel_type, 0)
        bus_emission = km_bus * bus_factor

        # Train emissions  
        train_factor = TRANSPORT_FACTORS['train'].get(train_type, 0)
        train_emission = km_train * train_factor

        # Flight emissions
        flight_emission = (
            TRANSPORT_FACTORS['flight']['short'] * short_flights +
            TRANSPORT_FACTORS['flight']['medium'] * medium_flights +
            TRANSPORT_FACTORS['flight']['long'] * long_flights
        )

        total_emission = car_emission + bus_emission + train_emission + flight_emission
        
        breakdown = {
            'car': car_emission,
            'bus': bus_emission, 
            'train': train_emission,
            'flights': flight_emission
        }
        
        logger.info(f"Transport emissions calculated: {total_emission:.2f} kg CO2")
        
        return {
            'total': total_emission,
            'breakdown': breakdown,
            'inputs': {
                'km_car': km_car,
                'car_fuel_type': car_fuel_type,
                'km_bus': km_bus,
                'bus_fuel_type': bus_fuel_type,
                'km_train': km_train,
                'train_type': train_type,
                'flights': {'short': short_flights, 'medium': medium_flights, 'long': long_flights}
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating transport emissions: {e}")
        raise ValueError(f"Failed to calculate transport emissions: {e}")

def get_transport_total(result: Dict[str, Any]) -> float:
    """Extract total emissions from transport calculation result."""
    return result.get('total', 0.0)