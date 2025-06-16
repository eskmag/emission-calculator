# Emission Factor Sources

This document explains the sources and assumptions for the emission factors used in `emission_factors.yaml`.

---

## 🔹 Transport

### Car (Petrol & Diesel)
- **Source**: U.S. Energy Information Administration (EIA), DrivingTests NZ
- **Reference**: https://www.eia.gov/environment/emissions/co2_vol_mass.php
- **Notes**: 2.31 kg CO₂/L (petrol), 2.68 kg CO₂/L (diesel) are standard carbon content combustion factors.

### Bus (Diesel/Electric/Biofuel)
- **Source**: UK Government GHG Conversion Factors, Transport & Environment
- **Notes**:
  - Electric: ~0.05 kg CO₂/kWh assuming average European grid.
  - Biofuel assumed carbon-neutral if sourced sustainably.

### Train
- **Electric**: Assumes highly efficient rail systems (e.g., EU/Scandinavia) – 0.01 kg CO₂/kWh/passenger.
- **Diesel**: Assumed lower per-passenger emissions than car based on occupancy.
- **Source**: European Environment Agency (EEA), DEFRA.

### Flights
- **Short/Medium/Long**:
  - **Source**: ICAO Carbon Emissions Calculator (https://www.icao.int), Our World in Data
  - Includes radiative forcing multiplier for high-altitude emissions.
  - Rounded for calculator usability.

---

## 🔹 Diet

- **Source**: "Reducing food’s environmental impacts through producers and consumers" (Poore & Nemecek, 2018, Science)
- **Summary**:
  - High meat: 7.2 kg CO₂e/day
  - Average diet: 5.6 kg
  - Vegetarian: 3.8 kg
  - Vegan: 2.9 kg
- **Reference**: https://science.sciencemag.org/content/360/6392/987
- **Popular explainers**: BBC, Guardian, Our World in Data

---

## 🔹 Energy

- **Electricity**: 0.02 kg CO₂/kWh is an average across Europe (due to hydro, nuclear, renewables).
  - **Source**: European Environment Agency (EEA), IEA
- **Oil**: 0.267 kg CO₂/kWh from heating oil – UK and Norwegian emissions databases.
- **Gas**: 0.25 kg CO₂/kWh – consistent with methane combustion emissions.
- **Wood**: 0.018 kg CO₂/kWh – assumed low-carbon due to carbon cycle if sustainably sourced.

---

## 📌 Notes:
- Factors are generalized for European users.
- All values are per unit burned/consumed (liter, kWh, passenger-trip, or kg food).
- They are designed for educational and indicative carbon footprinting.
