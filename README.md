# 🌍 Carbon Footprint Calculator

This Streamlit-based app helps users estimate their **carbon emissions** from three key areas of daily life:

- **🚗 Transport** (car, bus, train, flights)
- **⚡ Energy** (electricity, gas, oil, wood)
- **🥗 Diet** (based on dietary patterns)

The goal is to raise awareness and provide actionable insights into personal CO₂ contributions.

---

## 📦 Features

### 🧮 Core Calculations
- ✅ Interactive input for transport, energy, and food consumption
- ✅ Instant calculation of CO₂ emissions using up-to-date emission factors
- ✅ Input validation with helpful warnings for unrealistic values
- ✅ Graphical breakdowns (bar chart and pie chart supported)
- ✅ Tips for reducing emissions in each category

### 🔐 User Management
- ✅ Secure user authentication with password hashing
- ✅ Personal profiles with customizable settings
- ✅ Individual data tracking and privacy protection
- ✅ Demo accounts for quick testing
- ✅ Admin panel for user management

### 📊 Analytics & Tracking
- ✅ Goal setting and progress tracking
- ✅ Historical data visualization
- ✅ Personalized recommendations
- ✅ Global emission comparisons
- ✅ Export functionality for personal records

### 🛡️ Security & Privacy
- ✅ Password hashing with salt
- ✅ Session-based authentication
- ✅ Data isolation per user
- ✅ Input validation and sanitization
- ✅ Secure local storage

---

## 🚀 Quick Start

### Demo Account
Want to try without creating an account? Use the "Create Demo Account" button for instant access with all features enabled.

### Regular Account
1. **Register**: Create an account with username and password
2. **Login**: Access your personalized dashboard
3. **Calculate**: Enter your monthly transport, energy, and food data
4. **Track**: Set goals and monitor your progress over time
5. **Improve**: Follow personalized recommendations to reduce emissions

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

### 3. Access the Application

- **Main App**: http://localhost:8501
- **Admin Panel**: Navigate to Admin Panel in the app (login: admin/admin123)

Make sure all pages and modules are placed in their respective folders as shown above.

---

## 🔐 Security

This application includes a secure authentication system with:

- **Password Hashing**: All passwords are securely hashed with salt
- **Session Management**: Secure user sessions with proper isolation
- **Input Validation**: All user inputs are validated and sanitized
- **Data Privacy**: Users only have access to their own data
- **Admin Tools**: User management and monitoring capabilities

For detailed security information, see [SECURITY.md](./SECURITY.md).

**⚠️ Important**: Change default admin credentials before production deployment!

---

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
