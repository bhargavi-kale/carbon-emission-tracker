"""Vehicle model and emissions lookup utilities.

This module contains the :class:`Vehicle` class which stores
basic vehicle metadata and is expected to fetch emissions or
fuel-efficiency data from an external API. Current network
interactions are placeholders.
"""

import csv

class Vehicle:
    """Represent a vehicle and its emissions-related attributes."""

    def __init__(self, make:str, model:str, year:int):
        """Initialize a :class:`Vehicle` instance.
        
        Parameters
        ----------
        make : str
            The vehicle's manufacturer (e.g., "Toyota").
        model : str
            The vehicle's model name (e.g., "Camry").
        year : int
            The vehicle's model year (e.g., 2020).
        """
        self.make = make
        self.model = model
        self.year = year
        self.economy_data = self.fetch_economy_data(make, model, year)
        self.economy_id = int(self.economy_data["id"]) if self.economy_data else None
        self.fuel_type = self.economy_data["fuelType1"] if self.economy_data else None  #Gasoline, Diesel, Electric

    

    @staticmethod
    def fetch_economy_data(make: str, model: str, year: int)->dict:
        """Fetch fuel/economy data for this vehicle from an API.
        
        Parameters
        ----------
        make : str
            The vehicle's manufacturer.
        model : str
            The vehicle's model name.
        year : int
            The vehicle's model year.
        
        Returns
        -------
        dict
            A dictionary of economy data for the vehicle, or None if not found.
        """
        csv_reader = csv.DictReader(open('data/vehicles.csv'))
        return next((row for row in csv_reader if row["make"] == make and row["model"] == model and row["year"] == str(year)), None)
    
        
    def to_dict(self)->dict:
        """
        Convert the Vehicle instance to a JSON-serializable dictionary.

        Returns
        -------
        dict
            A dictionary representation of the Vehicle instance.
        """
        return {
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "economy_id": self.economy_id
        }
    
    @staticmethod
    def from_dict(data: dict)-> 'Vehicle':
        """
        Create a Vehicle instance from a dictionary.

        Parameters
        ----------
        data : dict
            A dictionary containing vehicle attributes.

        Returns
        -------
        Vehicle
            A new Vehicle instance.
        """
        vehicle = Vehicle(
            make=data["make"],
            model=data["model"],
            year=data["year"]
        )
        return vehicle