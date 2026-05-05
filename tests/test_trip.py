"""
Unit tests for the trip emissions logic.
"""

from src.trip import calculate_emissions

def test_gasoline_emissions():
    """
    HAPPY PATH: Test the standard emissions calculation for Gasoline.
    (100 miles / 25 mpg) * 19.6 = 78.4 lbs CO2.
    """
    result = calculate_emissions(100, "Gasoline", 25)
    assert round(result, 2) == 78.4


def test_premium_gasoline_emissions_happy_path():
    """
    HAPPY PATH: Test the emissions calculation for Premium Gasoline.
    (100 miles / 25 mpg) * 19.4 = 77.6 lbs CO2.
    """
    result = calculate_emissions(100, "Premium Gasoline", 25)
    assert round(result, 2) == 77.6

def test_diesel_emissions_happy_path():
    """
    HAPPY PATH: Test the emissions calculation for Diesel.
    (100 miles / 25 mpg) * 22.4 = 89.6 lbs CO2.
    """
    result = calculate_emissions(100, "Diesel", 25)
    assert round(result, 2) == 89.6

def test_unknown_fuel_type():
    """
    EDGE CASE: Test the fallback logic when an unsupported fuel type is provided.
    The system should use a default emission factor of 20 rather than 
    crashing or returning None.
    """
    result = calculate_emissions(100, "Hybrid", 25)
    # Default case: (100 / 25) * 20 = 80.0 lbs CO2
    assert result == 80.0

def test_zero_distance():
    """
    EDGE CASE: Test the behavior when the travel distance is zero.
    """
    result = calculate_emissions(0, "Gasoline", 25)
    assert result == 0

