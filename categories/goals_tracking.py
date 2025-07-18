import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
from main.utils.validators import validate_and_show_warning, validate_positive_number
from main.utils.supabase_auth import get_supabase_auth, get_current_user, is_authenticated

st.set_page_config(
    page_title="Goals & Progress Tracking",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎯 Carbon Reduction Goals & Progress")

st.title("🎯 Carbon Reduction Goals & Progress")

# Check authentication
if not is_authenticated():
    st.warning("Please login to access goal tracking.")
    st.stop()

username = get_current_user()
auth = get_supabase_auth()

# Load goals from database
user_goals = auth.get_user_goals()
if user_goals:
    if 'carbon_goals' not in st.session_state:
        st.session_state['carbon_goals'] = user_goals
else:
    # Initialize default goals if none exist
    if 'carbon_goals' not in st.session_state:
        st.session_state['carbon_goals'] = {
            'annual_target': 2000,  # kg CO2 per year
            'monthly_target': 167,  # kg CO2 per month
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'target_date': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        }

# Initialize progress data (will be loaded from database in future)
if 'progress_data' not in st.session_state:
    st.session_state['progress_data'] = []

# Goal Setting Section
st.subheader("🎯 Set Your Carbon Reduction Goals")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Current Goals:**")
    current_annual = st.session_state['carbon_goals']['annual_target']
    current_monthly = st.session_state['carbon_goals']['monthly_target']
    
    new_annual_target = st.number_input(
        "Annual CO₂ Target (kg):", 
        min_value=500, 
        max_value=20000, 
        value=current_annual,
        help="Paris Agreement target: ~2000 kg/year"
    )
    
    new_monthly_target = st.number_input(
        "Monthly CO₂ Target (kg):", 
        min_value=50, 
        max_value=2000, 
        value=current_monthly
    )

with col2:
    st.markdown("**Benchmark Targets:**")
    st.info("🌍 **Global Average**: 10,000 kg CO₂/year")
    st.info("🇪🇺 **EU Average**: 8,000 kg CO₂/year") 
    st.success("🎯 **Paris Agreement**: 2,000 kg CO₂/year")
    st.success("✨ **Climate Hero**: 1,000 kg CO₂/year")

if st.button("Update Goals"):
    # Validate goal inputs
    validation_errors = []
    
    if not validate_and_show_warning(new_annual_target, lambda x: validate_positive_number(x, "Annual target"), "Annual target", st):
        validation_errors.append("annual target")
    if not validate_and_show_warning(new_monthly_target, lambda x: validate_positive_number(x, "Monthly target"), "Monthly target", st):
        validation_errors.append("monthly target")
    
    # Check if targets are realistic
    if new_annual_target < 500:
        st.warning("⚠️ Annual target seems very low. Consider a more realistic goal.")
    if new_annual_target > 50000:
        st.warning("⚠️ Annual target seems very high. Consider a more ambitious goal.")
    
    if not validation_errors:
        # Save goals to database
        goals_data = {
            'annual_target': new_annual_target,
            'monthly_target': new_monthly_target,
            'updated_date': datetime.now().isoformat()
        }
        
        if auth.save_user_goals(goals_data):
            st.session_state['carbon_goals'].update({
                'annual_target': new_annual_target,
                'monthly_target': new_monthly_target,
            })
            st.success("Goals updated successfully!")
        else:
            st.error("Failed to save goals. Please try again.")
    else:
        st.error(f"Please check your input for: {', '.join(validation_errors)}")

st.divider()

# Current Progress
st.subheader("📊 Current Month Progress")

# Get current emissions
transport = st.session_state.get("transport_emissions", 0.0)
energy = st.session_state.get("energy_emissions", 0.0)
food = st.session_state.get("food_emissions", 0.0)
current_total = transport + energy + food

target = st.session_state['carbon_goals']['monthly_target']

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current Emissions", f"{current_total:.1f} kg CO₂")

with col2:
    st.metric("Monthly Target", f"{target:.1f} kg CO₂")

with col3:
    difference = current_total - target
    if difference > 0:
        st.metric("Over Target", f"+{difference:.1f} kg CO₂", delta=f"{difference:.1f}")
    else:
        st.metric("Under Target", f"{abs(difference):.1f} kg CO₂", delta=f"{difference:.1f}")

with col4:
    if target > 0:
        progress_pct = (current_total / target) * 100
        st.metric("Progress %", f"{progress_pct:.1f}%")

# Progress visualization
if current_total > 0:
    progress_df = pd.DataFrame({
        'Category': ['Current Emissions', 'Remaining to Target'],
        'Amount': [min(current_total, target), max(0, target - current_total)]
    })
    
    if current_total > target:
        progress_df = pd.DataFrame({
            'Category': ['Target', 'Over Target'],
            'Amount': [target, current_total - target]
        })
    
    fig = px.pie(progress_df, values='Amount', names='Category', 
                title=f"Progress vs Target ({target:.1f} kg CO₂)",
                color_discrete_map={'Current Emissions': '#2ca02c', 'Remaining to Target': '#d3d3d3',
                                  'Target': '#2ca02c', 'Over Target': '#ff4444'})
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Action Plan Generator
st.subheader("📋 Personalized Action Plan")

if current_total > target:
    reduction_needed = current_total - target
    st.warning(f"⚠️ You need to reduce {reduction_needed:.1f} kg CO₂ to meet your monthly target.")
    
    # Generate specific recommendations
    st.markdown("**Recommended Actions:**")
    
    # Transport recommendations
    if transport > current_total * 0.3:
        transport_reduction = min(reduction_needed * 0.4, transport * 0.3)
        st.markdown(f"""
        🚗 **Transport ({transport:.1f} kg CO₂)**: Target reduction: {transport_reduction:.1f} kg
        - Walk/cycle for trips under 5km (saves ~2-4 kg CO₂ per trip)
        - Use public transport for 2-3 car trips (saves ~3-8 kg CO₂ per trip)
        - Combine errands into one trip
        """)
    
    # Energy recommendations  
    if energy > current_total * 0.3:
        energy_reduction = min(reduction_needed * 0.3, energy * 0.25)
        st.markdown(f"""
        ⚡ **Energy ({energy:.1f} kg CO₂)**: Target reduction: {energy_reduction:.1f} kg
        - Lower thermostat by 2°C (saves ~15-20 kg CO₂/month)
        - Switch to LED bulbs (saves ~2-5 kg CO₂/month)
        - Unplug devices when not in use (saves ~3-8 kg CO₂/month)
        """)
    
    # Food recommendations
    if food > current_total * 0.3:
        food_reduction = min(reduction_needed * 0.3, food * 0.2)
        st.markdown(f"""
        🥗 **Food ({food:.1f} kg CO₂)**: Target reduction: {food_reduction:.1f} kg
        - Replace 1 beef meal with chicken (saves ~15-20 kg CO₂)
        - Try 2 plant-based meals per week (saves ~10-15 kg CO₂)
        - Reduce food waste by 25% (saves ~5-10 kg CO₂)
        """)

else:
    st.success(f"🎉 Congratulations! You're {target - current_total:.1f} kg CO₂ under your monthly target!")
    st.markdown("""
    **Keep up the great work! Consider:**
    - Setting a more ambitious target
    - Helping others reduce their emissions
    - Sharing your success story
    """)

# Save current calculation to progress
if st.button("Save Current Progress", type="primary"):
    if current_total > 0:
        progress_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'transport': transport,
            'energy': energy,
            'food': food,
            'total': current_total,
            'target': target,
            'met_target': current_total <= target
        }
        
        if 'progress_data' not in st.session_state:
            st.session_state['progress_data'] = []
        
        st.session_state['progress_data'].append(progress_entry)
        st.success("Progress saved! Check the Historical Progress section below.")
    else:
        st.warning("Please calculate your emissions first in other sections.")

st.divider()

# Historical Progress (if any data exists)
if st.session_state.get('progress_data'):
    st.subheader("📈 Historical Progress")
    
    df_progress = pd.DataFrame(st.session_state['progress_data'])
    df_progress['date'] = pd.to_datetime(df_progress['date'])
    
    # Line chart of progress over time
    fig_progress = px.line(df_progress, x='date', y=['total', 'target'], 
                          title="Emissions vs Target Over Time",
                          labels={'value': 'kg CO₂', 'date': 'Date'})
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Progress statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_emissions = df_progress['total'].mean()
        st.metric("Average Emissions", f"{avg_emissions:.1f} kg CO₂")
    
    with col2:
        targets_met = df_progress['met_target'].sum()
        total_entries = len(df_progress)
        success_rate = (targets_met / total_entries) * 100
        st.metric("Target Success Rate", f"{success_rate:.1f}%")
    
    with col3:
        if len(df_progress) > 1:
            trend = df_progress['total'].iloc[-1] - df_progress['total'].iloc[0]
            st.metric("Overall Trend", f"{trend:+.1f} kg CO₂")

# Export progress data
if st.session_state.get('progress_data'):
    st.subheader("📥 Export Progress Data")
    
    if st.button("Generate Progress Report"):
        df_export = pd.DataFrame(st.session_state['progress_data'])
        csv = df_export.to_csv(index=False)
        
        st.download_button(
            label="📊 Download Progress CSV",
            data=csv,
            file_name=f"carbon_progress_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )
