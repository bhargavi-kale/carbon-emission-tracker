"""CO₂ emissions calculator using distance, MPG, and fuel-type emission factors."""

def calculate_emissions(distance, fuel_type, mpg):
    """Estimate CO2 emissions for this trip.

    Returns
    -------
    float
        Estimated total emissions for the trip in lbs CO2.
    """
    gallons_used = distance / mpg
    if fuel_type == "Gasoline":
        total_emissions = (
            gallons_used * 19.6
        )  # Assuming 19.6 lbs CO2 per gallon of gasoline
    elif fuel_type == "Premium Gasoline":
        total_emissions = (
            gallons_used * 19.4
        )  # Assuming 19.4 lbs CO2 per gallon of premium gasoline
    elif fuel_type == "Diesel":
        total_emissions = (
            gallons_used * 22.4
        )  # Assuming 22.4 lbs CO2 per gallon of diesel
    elif fuel_type == "Electric":
        total_emissions = (
            0  # Electric vehicles assumed to have zero emissions for this placeholder
        )
    else:
        print(f"Unknown fuel type {fuel_type}, using default emission factor.")
        total_emissions = gallons_used * 20  # Default case for unknown fuel types
    return total_emissions
