"""Data models for emission calculations using Pydantic."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class TransportData(BaseModel):
    """Transport emission calculation data."""
    km_car: float = Field(ge=0, description="Kilometers traveled by car")
    car_fuel_type: str = Field(..., description="Type of car fuel")
    km_bus: float = Field(ge=0, description="Kilometers traveled by bus")
    bus_fuel_type: str = Field(..., description="Type of bus fuel")
    km_train: float = Field(ge=0, description="Kilometers traveled by train")
    train_type: str = Field(..., description="Type of train")
    short_flights: int = Field(ge=0, description="Number of short flights")
    medium_flights: int = Field(ge=0, description="Number of medium flights")
    long_flights: int = Field(ge=0, description="Number of long flights")
    
    @validator('car_fuel_type')
    def validate_car_fuel(cls, v):
        allowed = ['petrol', 'diesel', 'electric']
        if v.lower() not in allowed:
            raise ValueError(f'Car fuel type must be one of {allowed}')
        return v.lower()

class EnergyData(BaseModel):
    """Energy emission calculation data."""
    kwh_electricity: float = Field(ge=0, default=0)
    kwh_oil: float = Field(ge=0, default=0)
    kwh_gas: float = Field(ge=0, default=0)
    kwh_wood: float = Field(ge=0, default=0)

class FoodData(BaseModel):
    """Food emission calculation data."""
    diet_type: str = Field(..., description="Type of diet")
    
    @validator('diet_type')
    def validate_diet(cls, v):
        allowed = ['high_meat', 'average', 'vegetarian', 'vegan']
        if v.lower() not in allowed:
            raise ValueError(f'Diet type must be one of {allowed}')
        return v.lower()

class EmissionReport(BaseModel):
    """Complete emission calculation report."""
    transport_emissions: float
    energy_emissions: float
    food_emissions: float
    total_emissions: float
    calculation_date: datetime = Field(default_factory=datetime.now)
    
    @property
    def annual_projection(self) -> float:
        """Project annual emissions based on monthly data."""
        return self.total_emissions * 12
