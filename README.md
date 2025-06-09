```markdown
# Emission Calculator

**Emission Calculator** is a simple and extensible Python-based tool for estimating individual CO₂ emissions based on lifestyle and daily habits such as transport, diet, and energy consumption.

---

## 🌍 Features

- Estimate monthly CO₂ emissions from:
  - 🚗 Transportation (car, bus, flight)
  - 🥗 Diet (vegan, vegetarian, average, high-meat)
  - 🔌 Energy usage (electricity, oil, gas, wood)
- Modular structure, ready for expansion (e.g., consumption, waste)
- Unit tested for reliability
- CLI (Command-Line Interface) planned
- Web frontend planned

---

## 🧪 Running Tests

Make sure you're in the project root folder and run:

```bash
python -m unittest discover tests
```

---

## 🧠 Emission Factors and Sources

All emission factors used in this calculator are based on scientific studies and public data. These are general estimates and not meant to represent precise personal footprints.

### 🥩 Food Emissions (kg CO₂e per person per day)

| Diet Type  | Daily CO₂ | Monthly CO₂ | Source                                             |
| ---------- | --------- | ----------- | -------------------------------------------------- |
| High meat  | 7.2       | \~216 kg    | Poore & Nemecek (Science, 2018); Oxford University |
| Average    | 5.6       | \~168 kg    | BBC Climate Calculator; WWF; Oxford                |
| Vegetarian | 3.8       | \~114 kg    | EAT-Lancet, Oxford                                 |
| Vegan      | 2.9       | \~87 kg     | Poore & Nemecek; EAT-Lancet                        |

### 🔌 Energy Emissions (kg CO₂ per kWh)

| Energy Type          | Emission Factor | Source                                                 |
| -------------------- | --------------- | ------------------------------------------------------ |
| Electricity (Norway) | 0.02            | Statistics Norway (SSB), Statnett                      |
| Oil heating          | 0.27            | Miljødirektoratet (Norwegian Environment Agency)       |
| Gas heating          | 0.25            | NVE (Norwegian Water Resources and Energy Directorate) |
| Wood (biomass)       | 0.018           | EU RED II, Norwegian climate policy                    |

> Note: Electricity in Norway is almost 100% renewable (hydropower), resulting in very low CO₂ emissions.

---

## 📁 Project Structure

```
emission-calculator/
├── emission_calculator/
│   ├── calculator.py         # Emission calculation logic
│   ├── cli.py                # Command-line interface (in development)
│   ├── user_input.py         # Input helpers (planned)
│   ├── utils.py              # Common utilities (optional)
│   └── __init__.py
├── tests/
│   ├── test_calculator.py    # Unit tests
│   └── __init__.py
├── README.md
└── requirements.txt
```

---

## 🏗️ Roadmap

* [x] Add transport, diet, and energy emissions
* [ ] Add shopping and waste emissions
* [ ] Build CLI for user input
* [ ] Create web interface using Flask or React
* [ ] Add configuration for regional emission factors
* [ ] Visualize results with graphs

---

## 📜 License

This project is licensed under the MIT License.

---

## 👤 Author

Eskil – Informatics student @ University of Bergen (UiB)

```
