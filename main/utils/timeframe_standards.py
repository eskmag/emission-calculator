"""
Timeframe Standardization for Carbon Emission Calculator

This module ensures all calculations are standardized to MONTHLY timeframes.

STANDARD TIMEFRAMES:
- All user inputs should be monthly
- All calculations return monthly emissions (kg CO2 per month)
- All display outputs show monthly values
- Annual projections are calculated by multiplying monthly by 12

CONVERSION FACTORS:
- Daily to Monthly: × 30.44 (average days per month)
- Weekly to Monthly: × 4.33 (average weeks per month)
- Monthly to Annual: × 12
- Annual to Monthly: ÷ 12

SECTION STANDARDS:
1. Transport: Monthly km driven, monthly flights
2. Energy: Monthly kWh consumption  
3. Food: Monthly emissions based on diet type
4. Results: Monthly totals with annual projections
"""

from typing import Dict, Any

# Standard conversion factors
DAYS_PER_MONTH = 30.44
WEEKS_PER_MONTH = 4.33
MONTHS_PER_YEAR = 12

def daily_to_monthly(daily_value: float) -> float:
    """Convert daily value to monthly equivalent."""
    return daily_value * DAYS_PER_MONTH

def weekly_to_monthly(weekly_value: float) -> float:
    """Convert weekly value to monthly equivalent."""
    return weekly_value * WEEKS_PER_MONTH

def monthly_to_annual(monthly_value: float) -> float:
    """Convert monthly value to annual equivalent."""
    return monthly_value * MONTHS_PER_YEAR

def annual_to_monthly(annual_value: float) -> float:
    """Convert annual value to monthly equivalent."""
    return annual_value / MONTHS_PER_YEAR

def validate_timeframe_consistency(emissions_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that all emission data is in consistent monthly timeframes.
    
    Args:
        emissions_data: Dictionary containing emission values
        
    Returns:
        Dictionary with validation results and standardized values
    """
    result = {
        'is_consistent': True,
        'standardized_data': {},
        'warnings': []
    }
    
    for key, value in emissions_data.items():
        if isinstance(value, (int, float)):
            # All values should be reasonable monthly amounts
            if value < 0:
                result['warnings'].append(f"{key}: Negative value detected ({value})")
                result['is_consistent'] = False
            elif value > 10000:  # Very high monthly emissions
                result['warnings'].append(f"{key}: Unusually high monthly value ({value} kg CO2)")
            
            result['standardized_data'][key] = value
        else:
            result['standardized_data'][key] = value
    
    return result

def format_emission_display(value: float, timeframe: str = 'monthly') -> str:
    """
    Format emission value for display with appropriate timeframe label.
    
    Args:
        value: Emission value in kg CO2
        timeframe: Timeframe for display ('monthly', 'annual', 'daily')
        
    Returns:
        Formatted string for display
    """
    if timeframe == 'monthly':
        return f"{value:.1f} kg CO₂/month"
    elif timeframe == 'annual':
        return f"{value:.1f} kg CO₂/year"
    elif timeframe == 'daily':
        return f"{value:.1f} kg CO₂/day"
    else:
        return f"{value:.1f} kg CO₂"

def get_timeframe_help_text(section: str) -> str:
    """
    Get help text explaining timeframe expectations for each section.
    
    Args:
        section: Section name ('transport', 'energy', 'food')
        
    Returns:
        Help text string
    """
    help_texts = {
        'transport': "Enter your typical monthly transportation usage. For flights, use average monthly flights (e.g., 2 flights per year = 0.17 flights per month)",
        'energy': "Enter your monthly energy consumption from utility bills. Check your last monthly bill for kWh usage.",
        'food': "Select your typical diet type. The calculator uses standard monthly emission factors for each diet category."
    }
    
    return help_texts.get(section, "Enter monthly values for this category.")
