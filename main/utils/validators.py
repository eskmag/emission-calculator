"""Input validation utilities for the emission calculator."""

def validate_positive_number(value: float, field_name: str) -> bool:
    """Validate that a number is positive."""
    if value < 0:
        raise ValueError(f"{field_name} must be a positive number, got {value}")
    return True

def validate_km_input(km: float, max_reasonable: float = 10000) -> bool:
    """Validate kilometer input with reasonable limits."""
    validate_positive_number(km, "Distance")
    if km > max_reasonable:
        raise ValueError(f"Distance seems unusually high: {km} km. Please check your input.")
    return True

def validate_energy_input(kwh: float, max_reasonable: float = 5000) -> bool:
    """Validate energy consumption input."""
    validate_positive_number(kwh, "Energy consumption")
    if kwh > max_reasonable:
        raise ValueError(f"Energy consumption seems unusually high: {kwh} kWh. Please check your input.")
    return True

def validate_flights_input(flights: float, max_reasonable: float = 10) -> bool:
    """Validate flight input with reasonable limits."""
    validate_positive_number(flights, "Number of flights")
    if flights > max_reasonable:
        raise ValueError(f"Number of flights seems unusually high: {flights} flights per month. Please check your input.")
    return True

def validate_food_serving(servings: float, max_reasonable: float = 30) -> bool:
    """Validate food serving input."""
    validate_positive_number(servings, "Food servings")
    if servings > max_reasonable:
        raise ValueError(f"Food servings seem unusually high: {servings} servings per day. Please check your input.")
    return True

def validate_and_show_warning(value: float, validator_func, field_name: str, streamlit_container=None) -> bool:
    """
    Validate input and show warning in Streamlit if validation fails.
    Returns True if valid, False if invalid.
    """
    try:
        validator_func(value)
        return True
    except ValueError as e:
        if streamlit_container:
            streamlit_container.warning(f"⚠️ {str(e)}")
        return False
