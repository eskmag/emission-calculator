import streamlit as st
from main.core.food import food_emissions
from main.utils.validators import validate_and_show_warning, validate_food_serving
from main.utils.supabase_auth import get_supabase_auth, get_current_user, is_authenticated

st.set_page_config(
    page_title="Food Emissions",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🥗 Food Emissions Calculator")
st.markdown("""
    Welcome to the **Food Emissions Calculator!**
    Track your **monthly carbon footprint** from food with detailed breakdowns and personalized insights.
""")

st.divider()

# Food categories with detailed options
col1, col2 = st.columns(2)

with col1:
    st.subheader("🥩 Meat & Protein")
    
    # Meat consumption tracking
    beef_servings = st.slider("Beef servings per month:", 0, 60, 8, help="1 serving ≈ 100g")
    pork_servings = st.slider("Pork servings per month:", 0, 60, 4)
    chicken_servings = st.slider("Chicken servings per month:", 0, 60, 12)
    fish_servings = st.slider("Fish servings per month:", 0, 60, 8)
    
    # Plant-based proteins
    st.subheader("🌱 Plant-Based Proteins")
    legume_servings = st.slider("Legumes/beans servings per month:", 0, 60, 16)
    tofu_servings = st.slider("Tofu/tempeh servings per month:", 0, 60, 4)

with col2:
    st.subheader("🥛 Dairy & Eggs")
    milk_glasses = st.slider("Glasses of milk per day:", 0, 5, 1, help="1 glass ≈ 250ml")
    cheese_servings = st.slider("Cheese servings per month:", 0, 60, 12, help="1 serving ≈ 30g")
    eggs_per_month = st.slider("Eggs per month:", 0, 90, 16)
    
    st.subheader("🍎 Fruits & Vegetables")
    local_produce_pct = st.slider("% of produce that's local/seasonal:", 0, 100, 50)
    organic_pct = st.slider("% of food that's organic:", 0, 100, 20)

# Alternative: Quick diet type selection
st.divider()
st.subheader("🍽️ Quick Diet Type Selection")

diet_type = st.selectbox(
    "Or choose a general diet type:",
    options=[
        ("custom", "Custom (use sliders above)"),
        ("high_meat", "High Meat Diet"), 
        ("average", "Average Omnivore"), 
        ("vegetarian", "Vegetarian"), 
        ("vegan", "Vegan")
    ],
    format_func=lambda x: x[1]
)

# Calculate emissions based on input method
if st.button("Calculate Food Emissions", type="primary"):
    # Validate inputs if using custom mode
    if diet_type[0] == "custom":
        validation_errors = []
        
        # Validate serving inputs
        servings_to_validate = [
            (beef_servings, "Beef servings"),
            (pork_servings, "Pork servings"),
            (chicken_servings, "Chicken servings"),
            (fish_servings, "Fish servings"),
            (legume_servings, "Legume servings"),
            (tofu_servings, "Tofu servings"),
            (milk_glasses, "Milk glasses"),
            (cheese_servings, "Cheese servings"),
            (eggs_per_month, "Eggs per month")
        ]
        
        for serving_value, field_name in servings_to_validate:
            if not validate_and_show_warning(serving_value, validate_food_serving, field_name, st):
                validation_errors.append(field_name.lower())
        
        if validation_errors:
            st.error(f"Please check your input for: {', '.join(validation_errors)}")
            st.stop()
    
    try:
        if diet_type[0] == "custom":
            # Detailed calculation based on specific foods
            # Emission factors (kg CO2 per serving)
            FOOD_EMISSIONS = {
                'beef': 6.6,        # kg CO2 per 100g serving
                'pork': 2.9,
                'chicken': 1.6,
                'fish': 1.2,
                'legumes': 0.1,
                'tofu': 0.3,
                'milk': 0.4,        # per 250ml glass
                'cheese': 1.0,      # per 30g serving
                'eggs': 0.4         # per egg
            }
            
            monthly_emissions = (
                beef_servings * FOOD_EMISSIONS['beef'] +
                pork_servings * FOOD_EMISSIONS['pork'] +
                chicken_servings * FOOD_EMISSIONS['chicken'] +
                fish_servings * FOOD_EMISSIONS['fish'] +
                legume_servings * FOOD_EMISSIONS['legumes'] +
                tofu_servings * FOOD_EMISSIONS['tofu'] +
                (milk_glasses * 30.44) * FOOD_EMISSIONS['milk'] +  # Daily to monthly
                cheese_servings * FOOD_EMISSIONS['cheese'] +
                eggs_per_month * FOOD_EMISSIONS['eggs']
            )
            
            # Apply modifiers for local/organic food
            local_reduction = (local_produce_pct / 100) * 0.15  # 15% reduction for local
            organic_reduction = (organic_pct / 100) * 0.05      # 5% reduction for organic
            
            total_reduction = min(local_reduction + organic_reduction, 0.25)  # Max 25% reduction
            monthly_emissions = monthly_emissions * (1 - total_reduction)
            
            # Detailed breakdown
            st.subheader("📊 Detailed Food Emissions Breakdown")
            
            breakdown_data = {
                'Food Category': ['Beef', 'Pork', 'Chicken', 'Fish', 'Legumes', 'Tofu', 'Milk', 'Cheese', 'Eggs'],
                'Monthly Servings': [beef_servings, pork_servings, chicken_servings, fish_servings, 
                                   legume_servings, tofu_servings, milk_glasses*30.44, cheese_servings, eggs_per_month],
                'Monthly Emissions (kg CO₂)': [
                    beef_servings * FOOD_EMISSIONS['beef'],
                    pork_servings * FOOD_EMISSIONS['pork'], 
                    chicken_servings * FOOD_EMISSIONS['chicken'],
                    fish_servings * FOOD_EMISSIONS['fish'],
                    legume_servings * FOOD_EMISSIONS['legumes'],
                    tofu_servings * FOOD_EMISSIONS['tofu'],
                    (milk_glasses * 30.44) * FOOD_EMISSIONS['milk'],
                    cheese_servings * FOOD_EMISSIONS['cheese'],
                    eggs_per_month * FOOD_EMISSIONS['eggs']
                ]
            }
            
            import pandas as pd
            df_breakdown = pd.DataFrame(breakdown_data)
            df_breakdown = df_breakdown[df_breakdown['Monthly Servings'] > 0]  # Only show consumed items
            
            if not df_breakdown.empty:
                st.dataframe(df_breakdown, use_container_width=True)
                
                # Visual breakdown
                import plotly.express as px
                fig = px.bar(df_breakdown, x='Food Category', y='Monthly Emissions (kg CO₂)',
                            title="Monthly Food Emissions by Category")
                st.plotly_chart(fig, use_container_width=True)
            
            food_emissions_result = monthly_emissions
            
        else:
            # Use simple diet type calculation
            food_emissions_result = food_emissions(diet_type=diet_type[0])
        
        st.success(f"✅ Calculation complete!")
        
        # Results display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Monthly Food Emissions", f"{food_emissions_result:.1f} kg CO₂")
        
        with col2:
            st.metric("Daily Average", f"{food_emissions_result/30:.1f} kg CO₂")
        
        with col3:
            annual_projection = food_emissions_result * 12
            st.metric("Annual Projection", f"{annual_projection:.1f} kg CO₂")
        
        # Store in session state
        st.session_state["food_emissions"] = food_emissions_result
        
        # Save to database if user is authenticated
        if is_authenticated():
            auth = get_supabase_auth()
            emission_details = {
                'diet_type': diet_type[0],
                'beef_servings': beef_servings if diet_type[0] == "custom" else 0,
                'pork_servings': pork_servings if diet_type[0] == "custom" else 0,
                'chicken_servings': chicken_servings if diet_type[0] == "custom" else 0,
                'fish_servings': fish_servings if diet_type[0] == "custom" else 0,
                'legume_servings': legume_servings if diet_type[0] == "custom" else 0,
                'tofu_servings': tofu_servings if diet_type[0] == "custom" else 0,
                'milk_glasses': milk_glasses if diet_type[0] == "custom" else 0,
                'cheese_servings': cheese_servings if diet_type[0] == "custom" else 0,
                'eggs_per_month': eggs_per_month if diet_type[0] == "custom" else 0,
                'local_produce_pct': local_produce_pct if diet_type[0] == "custom" else 0,
                'organic_pct': organic_pct if diet_type[0] == "custom" else 0,
                'calculation_date': str(st.session_state.get('calculation_date', ''))
            }
            
            if auth.save_user_emissions('food', food_emissions_result, emission_details):
                st.success("✅ Food emissions saved to your profile!")
            else:
                st.warning("Could not save food emissions to database.")
        
        # Comparison and tips
        st.subheader("🌱 Improvement Suggestions")
        
        if food_emissions_result > 150:
            st.warning("🔴 Your food emissions are quite high. Consider these changes:")
            st.markdown("""
            - **Reduce red meat**: Replace 1-2 beef meals per week with chicken or plant-based alternatives
            - **Try plant-based proteins**: Incorporate more legumes, tofu, and nuts
            - **Choose local produce**: Reduce transportation emissions by 10-15%
            """)
        elif food_emissions_result > 100:
            st.info("🟡 Your food emissions are moderate. Small changes can make a big difference:")
            st.markdown("""
            - **Meatless Mondays**: Try one plant-based day per week
            - **Seasonal eating**: Choose fruits and vegetables in season
            - **Reduce food waste**: Plan meals and store food properly
            """)
        else:
            st.success("🟢 Great job! Your food emissions are relatively low.")
            st.markdown("""
            - **Keep it up**: Your current diet has a low carbon footprint
            - **Share knowledge**: Help others reduce their food emissions
            - **Consider organic**: Support sustainable farming practices
            """)
            
    except Exception as e:
        st.error(f"Error calculating food emissions: {str(e)}")
        st.info("Please check your inputs and try again.")
    
    with col2:
        st.metric("Daily Average", f"{food_emissions_result/30:.1f} kg CO₂")
    
    with col3:
        annual_projection = food_emissions_result * 12
        st.metric("Annual Projection", f"{annual_projection:.1f} kg CO₂")
    
    # Comparison and tips
    st.subheader("🌱 Improvement Suggestions")
    
    if food_emissions_result > 150:
        st.warning("🔴 Your food emissions are quite high. Consider these changes:")
        st.markdown("""
        - **Reduce red meat**: Replace 1-2 beef meals per week with chicken or plant-based alternatives
        - **Try plant-based proteins**: Incorporate more legumes, tofu, and nuts
        - **Choose local produce**: Reduce transportation emissions by 10-15%
        """)
    elif food_emissions_result > 100:
        st.info("🟡 Your food emissions are moderate. Small changes can make a big difference:")
        st.markdown("""
        - **Meatless Mondays**: Try one plant-based day per week
        - **Seasonal eating**: Choose fruits and vegetables in season
        - **Reduce food waste**: Plan meals and store food properly
        """)
    else:
        st.success("🟢 Great job! Your food emissions are relatively low.")
        st.markdown("""
        - **Keep it up**: Your current diet has a low carbon footprint
        - **Share knowledge**: Help others reduce their food emissions
        - **Consider organic**: Support sustainable farming practices
        """)
    
    # Store in session state
    st.session_state["food_emissions"] = food_emissions_result

st.divider()

# Food tips and information
st.subheader("📚 Food Carbon Footprint Guide")

with st.expander("🥩 Meat & Fish Carbon Impact"):
    st.markdown("""
    **High Impact (kg CO₂ per 100g):**
    - Beef: 6.6 kg CO₂
    - Lamb: 5.5 kg CO₂
    - Pork: 2.9 kg CO₂
    
    **Medium Impact:**
    - Chicken: 1.6 kg CO₂
    - Fish (farmed): 1.2 kg CO₂
    - Fish (wild): 0.8 kg CO₂
    
    **Low Impact:**
    - Legumes: 0.1 kg CO₂
    - Tofu: 0.3 kg CO₂
    - Nuts: 0.2 kg CO₂
    """)

with st.expander("🥛 Dairy Impact"):
    st.markdown("""
    - Cheese: 1.0 kg CO₂ per 30g serving
    - Milk: 0.4 kg CO₂ per 250ml glass
    - Yogurt: 0.3 kg CO₂ per 150g serving
    - Butter: 2.4 kg CO₂ per 100g
    
    **Plant-based alternatives typically have 50-80% lower emissions**
    """)

with st.expander("🌍 Sustainable Food Tips"):
    st.markdown("""
    1. **Eat seasonally**: Reduces transportation and storage emissions
    2. **Choose local**: Support local farmers and reduce transport emissions
    3. **Reduce waste**: 1/3 of food is wasted globally
    4. **Grow your own**: Even herbs on a windowsill help
    5. **Cook at home**: Processed foods have higher emissions
    6. **Meal planning**: Reduces impulse purchases and waste
    """)
