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
    def prompt()-> 'Vehicle':
        """Prompt the user for vehicle details and return a Vehicle instance.
        
        Returns
        -------
        Vehicle
            A new Vehicle instance based on user input.
        """
        make = input("Enter vehicle make: ")
        model = input("Enter vehicle model: ")
        year = int(input("Enter vehicle year: "))
        return Vehicle(make, model, year)
    
    def manage(self):
        """
        Prints out current vehicle information, and allows the user to update it.
        """

        for idx, attr in enumerate(["make", "model", "year"]):
            print(f"{idx + 1}. {attr.capitalize()}: {getattr(self, attr)}")
        print("0. Exit")
        
        while (choice := int(input("Select an attribute to update (or 0 to exit): "))):
            if choice < 1 or choice > 4:
                print("Invalid choice. Please try again.")
                continue
            attr = ["make", "model", "year"][choice - 1]
            new_value = input(f"Enter new value for {attr}: ")
            if attr == "year":
                new_value = int(new_value)
            setattr(self, attr, new_value)
            print(f"{attr.capitalize()} updated to {new_value}.")
            for idx, attr in enumerate(["make", "model", "year"]):
                print(f"{idx + 1}. {attr.capitalize()}: {getattr(self, attr)}")
            print("0: Exit")

            self.economy_data = self.fetch_economy_data(self.make, self.model, self.year)
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
    
    @staticmethod
    def economy_data_for_id(id: int)->dict:
        """
        Fetch fuel/economy data for a vehicle by its economy ID.

        Parameters
        ----------
        id : int
            The vehicle's economy ID.

        Returns
        -------
        dict
            A dictionary of economy data for the vehicle, or None if not found.
        """
        csv_reader = csv.DictReader(open('data/vehicles.csv'))
        return next((row for row in csv_reader if row["id"] == str(id)), None)
    
    def get_mpg(self, driving_type: str)->float:
        """Get the vehicle's MPG for a given driving type.

        Parameters
        ----------
        driving_type : str
            Either "city" or "highway".

        Returns
        -------
        float
            The MPG value for the specified driving type.
        """
        if driving_type == "city":
            return float(self.economy_data["city08"])
        elif driving_type == "highway":
            return float(self.economy_data["highway08"])
        else:
            return float(self.economy_data["comb08"])
        
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