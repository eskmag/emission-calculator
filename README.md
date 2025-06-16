# 🌍 Carbon Footprint Calculator

This Streamlit-based app helps users estimate their **carbon emissions** from three key areas of daily life:

- **🚗 Transport** (car, bus, train, flights)
- **⚡ Energy** (electricity, gas, oil, wood)
- **🥗 Diet** (based on dietary patterns)

The goal is to raise awareness and provide actionable insights into personal CO₂ contributions.

---

## 📦 Features

- ✅ Interactive input for transport, energy, and food consumption
- ✅ Instant calculation of CO₂ emissions using up-to-date emission factors
- ✅ Session-based memory of values between sections
- ✅ Graphical breakdowns (bar chart and pie chart supported)
- ✅ Tips for reducing emissions in each category

---


## 🧮 Emission Factors

Emission values are based on publicly available and peer-reviewed sources, including:

- [EIA](https://www.eia.gov/environment/emissions/co2_vol_mass.php)
- [European Environment Agency](https://www.eea.europa.eu/)
- [Poore & Nemecek, 2018, *Science*](https://science.sciencemag.org/content/360/6392/987)
- [ICAO Carbon Emissions Calculator](https://www.icao.int)

Detailed documentation available in [`emission_sources.md`](./emission_sources.md).

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```
### 2. Run the App

```bash
streamlit run streamlit_app.py
```
Make sure all pages and modules are placed in their respective folders as shown above.

📊 Example Visualizations
Bar chart showing transport vs energy vs food emissions

Summary of individual contributions in kg CO₂

Embedded tips for reducing each category's impact

---

## 📃 License
This project is licensed under the MIT License.

---

## 👤 Author

Eskil – Informatics student @ University of Bergen (UiB)
