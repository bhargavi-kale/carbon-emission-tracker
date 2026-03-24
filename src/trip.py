"""Trip representation and emissions calculation utilities.

The :class:`Trip` class couples a :class:`route.Route` and
:class:`vehicle.Vehicle` instance and provides a basic
method for computing estimated CO2 emissions for the trip.
"""


class Trip:
    """Represent a single trip and compute its emissions.

    Parameters
    ----------
    route : Route
        A :class:`Route` instance describing origin, destination and distance.
    vehicle : Vehicle
        A :class:`Vehicle` instance used for the trip.
    frequency : int, optional
        The frequency period in days (e.g., 7 for weekly), by default 0.
    occurance : int, optional
        Number of occurrences of the trip within the frequency period.
    passengers : int, optional
        Number of passengers occupying the vehicle for the trip.
    """

    def __init__(self, route, vehicle, frequency=0, occurrence=1, passengers=1):
        """Initialize a :class:`Trip`.

        :param route Route: The route for the trip.
        :param vehicle Vehicle: The vehicle used for the trip.
        :param frequency int: Frequency period in days.
        :param occurance int: Number of occurrences within the frequency.
        :param passengers int: Number of passengers for the trip.
        """
        self.route = route
        self.vehicle = vehicle
        self.frequency = frequency
        self.occurrence = occurrence
        self.passengers = passengers
        self.total_emissions = round(self.calculate_emissions(), 2)

    def calculate_emissions(self):
        """Estimate CO2 emissions for this trip.

        Returns
        -------
        float
            Estimated total emissions for the trip in lbs CO2.
        """
        distance = self.route.distance
        mpg = self.vehicle.get_mpg("city") # Placeholder, will select between city/highway later
        gallons_used = distance / mpg
        if self.vehicle.fuel_type == "Gasoline":
            total_emissions = (gallons_used * 19.6) / self.passengers  # Assuming 19.6 lbs CO2 per gallon of gasoline
        elif self.vehicle.fuel_type == "Premium Gasoline":
            total_emissions = (gallons_used * 19.4) / self.passengers  # Assuming 19.4 lbs CO2 per gallon of premium gasoline
        elif self.vehicle.fuel_type == "Diesel":
            total_emissions = (gallons_used * 22.4) / self.passengers  # Assuming 22.4 lbs CO2 per gallon of diesel
        elif self.vehicle.fuel_type == "Electric":
            total_emissions = 0  # Electric vehicles assumed to have zero emissions for this placeholder
        else:
            print(f"Unknown fuel type {self.vehicle.fuel_type}, using default emission factor.")
            total_emissions = (gallons_used * 20) / self.passengers  # Default case for unknown fuel types
        return total_emissions