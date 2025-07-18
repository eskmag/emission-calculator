import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Results & Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Results & Analytics")

# Quick navigation to categories
st.markdown("### 📋 Calculate Your Emissions:")
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("categories/transport.py", label="🚗 **Transport Emissions**", help="Calculate transport emissions")
with col2:
    st.page_link("categories/energy.py", label="⚡ **Energy Emissions**", help="Calculate energy emissions")
with col3:
    st.page_link("categories/enhanced_food.py", label="🥗 **Food Emissions**", help="Calculate food emissions")

st.divider()

# Get emissions from session state
transport = st.session_state.get("transport_emissions", 0.0)
energy = st.session_state.get("energy_emissions", 0.0)
food = st.session_state.get("food_emissions", 0.0)
total_emissions = transport + energy + food

# Global averages for comparison (monthly)
GLOBAL_AVERAGES = {
    "Global Average": 833,  # kg CO2 per month (10 tons per year)
    "EU Average": 667,      # kg CO2 per month (8 tons per year)
    "Paris Agreement Target": 167,  # kg CO2 per month (2 tons per year)
}

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Your Carbon Footprint")
    
    # Create emissions breakdown pie chart
    if total_emissions > 0:
        emission_data = pd.DataFrame({
            'Category': ['Transport', 'Energy', 'Food'],
            'Emissions': [transport, energy, food],
            'Percentage': [transport/total_emissions*100, energy/total_emissions*100, food/total_emissions*100]
        })
        
        fig = px.pie(emission_data, values='Emissions', names='Category', 
                    title="Monthly Emissions Breakdown",
                    color_discrete_map={'Transport': '#ff7f0e', 'Energy': '#2ca02c', 'Food': '#d62728'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Add horizontal bar chart
        emission_df = pd.DataFrame({
            "Emissions (kg CO₂)": [transport, energy, food]
        }, index=["Transport", "Energy", "Food"])
        
        st.subheader("Emissions by Category")
        st.bar_chart(emission_df, horizontal=True)
        
        # Also show the simple breakdown for comparison
        st.subheader("📋 Detailed Breakdown")
        st.markdown(f"""
        **Your total monthly emissions:** {total_emissions:.2f} kg CO₂
        
        **By Category:**
        - 🚗 **Transport**: {transport:.2f} kg CO₂ ({transport/total_emissions*100:.1f}%)
        - ⚡ **Energy**: {energy:.2f} kg CO₂ ({energy/total_emissions*100:.1f}%)
        - 🥗 **Food**: {food:.2f} kg CO₂ ({food/total_emissions*100:.1f}%)
        """)
    else:
        st.warning("⚠️ No emission data available. Please calculate your emissions in the category sections first.")
        st.info("👆 Use the links above to calculate your emissions for each category.")

with col2:
    st.subheader("Quick Stats")
    st.metric("Total Monthly Emissions", f"{total_emissions:.1f} kg CO₂")
    st.metric("Annual Projection", f"{total_emissions * 12:.1f} kg CO₂")
    st.metric("Daily Average", f"{total_emissions / 30:.1f} kg CO₂")
    
    # Carbon intensity rating
    if total_emissions <= 167:
        rating = "🟢 Excellent"
        color = "green"
    elif total_emissions <= 400:
        rating = "🟡 Good"
        color = "orange" 
    elif total_emissions <= 667:
        rating = "🟠 Average"
        color = "orange"
    else:
        rating = "🔴 High"
        color = "red"
    
    st.markdown(f"**Carbon Rating:** :{color}[{rating}]")

st.divider()

# Comparison with global averages
st.subheader("🌍 How You Compare")

comparison_data = pd.DataFrame({
    'Category': list(GLOBAL_AVERAGES.keys()) + ['Your Emissions'],
    'Monthly Emissions': list(GLOBAL_AVERAGES.values()) + [total_emissions]
})

fig_comparison = px.bar(comparison_data, x='Category', y='Monthly Emissions',
                       title="Your Emissions vs. Global Benchmarks",
                       color='Category',
                       color_discrete_map={'Your Emissions': '#1f77b4'})
fig_comparison.update_layout(showlegend=False)
st.plotly_chart(fig_comparison, use_container_width=True)

# Improvement suggestions
st.subheader("💡 Personalized Improvement Suggestions")

suggestions = []
if transport > total_emissions * 0.4:
    suggestions.append("🚗 **Transport** is your highest emission source. Consider public transport, cycling, or electric vehicles.")
if energy > total_emissions * 0.4:
    suggestions.append("⚡ **Energy** consumption is high. Consider renewable energy, better insulation, or energy-efficient appliances.")
if food > total_emissions * 0.4:
    suggestions.append("🥗 **Food** emissions are significant. Consider reducing meat consumption or choosing local, seasonal foods.")

if transport > 150:
    suggestions.append("🚶‍♂️ Try walking or cycling for short trips under 5km.")
if energy > 100:
    suggestions.append("🏠 Improve home insulation and use programmable thermostats.")
if food > 120:
    suggestions.append("🌱 Try 'Meatless Mondays' or plant-based meals 2-3 times per week.")

if suggestions:
    for suggestion in suggestions:
        st.markdown(f"- {suggestion}")
else:
    st.success("🎉 Great job! Your emissions are quite low. Keep up the good work!")

# Future projections
st.subheader("📈 Impact Projections")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**10% Reduction Scenario**")
    reduced_10 = total_emissions * 0.9
    st.metric("Monthly", f"{reduced_10:.1f} kg CO₂", f"-{total_emissions - reduced_10:.1f}")
    st.metric("Annual", f"{reduced_10 * 12:.1f} kg CO₂", f"-{(total_emissions - reduced_10) * 12:.1f}")

with col2:
    st.markdown("**25% Reduction Scenario**")
    reduced_25 = total_emissions * 0.75
    st.metric("Monthly", f"{reduced_25:.1f} kg CO₂", f"-{total_emissions - reduced_25:.1f}")
    st.metric("Annual", f"{reduced_25 * 12:.1f} kg CO₂", f"-{(total_emissions - reduced_25) * 12:.1f}")

with col3:
    st.markdown("**Paris Agreement Target**")
    target = 167
    st.metric("Monthly Target", f"{target} kg CO₂")
    if total_emissions > target:
        reduction_needed = ((total_emissions - target) / total_emissions) * 100
        st.metric("Reduction Needed", f"{reduction_needed:.1f}%")
    else:
        st.success("🎯 Target achieved!")

# Export functionality
st.subheader("📥 Export Your Data")
if st.button("Generate Detailed Report"):
    report_data = {
        'Calculation Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'Transport Emissions (kg CO₂)': transport,
        'Energy Emissions (kg CO₂)': energy,
        'Food Emissions (kg CO₂)': food,
        'Total Monthly Emissions (kg CO₂)': total_emissions,
        'Annual Projection (kg CO₂)': total_emissions * 12,
        'Carbon Rating': rating,
        'Comparison to Global Average': f"{((total_emissions / GLOBAL_AVERAGES['Global Average']) - 1) * 100:.1f}%"
    }
    
    df_report = pd.DataFrame([report_data])
    csv = df_report.to_csv(index=False)
    
    st.download_button(
        label="📊 Download CSV Report",
        data=csv,
        file_name=f"carbon_footprint_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )
