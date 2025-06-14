from pydantic import BaseModel


class EmissionRequest(BaseModel):
    km_car: float
    car_fuel_type: str
    km_bus: float
    bus_fuel_type: str
    km_train: float
    train_type: str
    short_flights: int
    medium_flights: int
    long_flights: int
    diet_type: str
    kwh_electricity: float
    kwh_oil: float
    kwh_gas: float
    kwh_wood: float

class EmissionResponse(BaseModel):
    transport: float
    food: float
    energy: float
    total: float