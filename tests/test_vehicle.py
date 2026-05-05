"""
Unit tests for the Vehicle class.
"""
from src.vehicle import Vehicle


def test_fetch_economy_data_valid():
    """
    HAPPY PATH: Test that fetch_economy_data returns a valid dictionary 
    when provided with a known make, model, and year from the dataset.
    """
    data = Vehicle.fetch_economy_data("Toyota", "Camry", 2020)
    assert data is not None
    assert "id" in data


def test_fetch_economy_data_invalid():
    """
    EDGE CASE: Test that fetch_economy_data returns None when provided 
    with credentials that do not exist (e.g., non-existent model or invalid make).
    This ensures the system handles missing data without crashing.
    """
    data = Vehicle.fetch_economy_data("xyz", "yxz", 1900)
    assert data is None
