from fastapi import APIRouter
from main.core.transport import transport_emissions
from main.core.food import food_emissions
from main.core.energy import energy_emissions
from main.models.api_models import EmissionRequest, EmissionResponse

router = APIRouter()


@router.post("/calculate", response_model=EmissionResponse)
def calculate_emissions(data: EmissionRequest):
    transport = transport_emissions(
        km_car=data.km_car,
        car_fuel_type=data.car_fuel_type,
        km_bus=data.km_bus,
        bus_fuel_type=data.bus_fuel_type,
        km_train=data.km_train,
        train_type=data.train_type,
        short_flights=data.short_flights,
        medium_flights=data.medium_flights,
        long_flights=data.long_flights
    )

    food = food_emissions(data.diet_type)

    energy = energy_emissions(
        electricity=data.kwh_electricity,
        oil=data.kwh_oil,
        gas=data.kwh_gas,
        wood=data.kwh_wood
    )

    total = transport + food + energy

    return EmissionResponse(
        transport=transport,
        food=food,
        energy=energy,
        total=total
    )