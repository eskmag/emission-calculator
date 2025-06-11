from dataclasses import dataclass

@dataclass
class EmissionProfile:
    km_car: float
    km_bus: float
    km_plane: float
    diet_type: str
    kwh_electricity: float
    kwh_oil: float
    kwh_gas: float
    kwh_wood: float

    def transport(self) -> float:
        from main.core.transport import transport_emissions
        return transport_emissions(self.km_car, self.km_bus, self.km_plane)
    
    def food(self) -> float:
        from main.core.food import food_emissions
        return food_emissions(self.diet_type)
    
    def energy(self) -> float:
        from main.core.energy import energy_emissions
        return energy_emissions(self.kwh_electricity, self.kwh_oil, self.kwh_gas, self.kwh_wood)
    
    def total(self) -> float:
        return self.transport() + self.food() + self.energy()