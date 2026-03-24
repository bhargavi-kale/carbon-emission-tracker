"""CLI and application control for the Carbon Commute calculator.

This module provides the :class:`CarbonCommute` class which implements
a minimal command-line interface for managing vehicles, trips and
producing simple summaries. The current implementation contains
placeholder I/O and persistence methods and is suitable for
interactive experimentation and further extension.
"""

from src.route import Route
from src.trip import Trip
from src.vehicle import Vehicle
import json
import os


class CarbonCommute:
    """Main application class handling I/O and program flow.

    The class holds in-memory lists of vehicles and trips and exposes
    methods for running a text-based menu, adding trips, and viewing
    simple emissions summaries.
    """

    def __init__(self):
        """Create a new CarbonCommute application instance."""
        self.vehicles = []
        """A list of vehicles available to the application."""
        self.trips = []

    def run(self):
        """Start the interactive application loop."""

        print("Welcome to the Carbon Commute Calculator!")
        while True:
            print("0. Load File")
            print("1. Add/Manage Vehicles")
            print("2. Add Trip")
            print("3. View Summary")
            print("4. Save Data")
            print("5. Exit")
    
            choice = input("Select an option: ")
            if choice == '0':
                self.load_file()
            elif choice == '1':
                self.manage_vehicles()
            elif choice == '2':
                self.calculator()
            elif choice == '3':
                self.view_summary()
            elif choice == '4':
                self.save_data()
            elif choice == '5':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")

    def calculator(self):
        """Interactively create a :class:`Trip` and add it to the app."""
        print("Please select a vehicle:")
        for idx, vehicle in enumerate(self.vehicles):
            print(f"{idx}. {vehicle.make} {vehicle.model} ({vehicle.year}) - {vehicle.fuel_type}")
        
        vehicle_choice = int(input("Enter the number for the vehicle: "))
        while vehicle_choice < 0 or vehicle_choice >= len(self.vehicles):
            vehicle_choice = int(input("Invalid choice. Enter the number of the vehicle: "))
        selected_vehicle = self.vehicles[vehicle_choice]
        
        origin = input("Enter the origin address: ")
        destination = input("Enter the destination address: ")
        route = Route(origin, destination)
        route.fetch_route_data()
        
        #Occurance is the number of times the trip occurs within the frequency (days) period.
        frequency = int(input("Enter the frequency of the trip in days (e.g., 7 for a week, 30 for a month): "))
        occurrence = int(input("Enter the number of times this trip occurs in the given frequency: "))
        passengers = int(input("Enter the number of passengers in the vehicle: "))

        trip = Trip(route, selected_vehicle, frequency, occurrence, passengers)
        self.trips.append(trip)

        print(f"Trip added! Total emissions for this trip: {trip.total_emissions} lbs CO2")

    def manage_vehicles(self):
        """Lists and allows management of vehicles in the application."""
        if (len(self.vehicles) == 0):
            self.vehicles.append(Vehicle.prompt())
        else:
            for idx, vehicle in enumerate(self.vehicles):
                print(f"{idx + 1}. {vehicle.make} {vehicle.model} ({vehicle.year}) - {vehicle.fuel_type}")
            print(f"{len(self.vehicles) + 1}. Add New Vehicle")
            print("0. Exit")
            while (choice := int(input("Enter 0 to exit or the number of a vehicle to manage: "))):
                if choice == len(self.vehicles) + 1:
                    self.vehicles.append(Vehicle.prompt())
                else:
                    self.vehicles[choice - 1].manage()
                for idx, vehicle in enumerate(self.vehicles):
                    print(f"{idx + 1}. {vehicle.make} {vehicle.model} ({vehicle.year}) - {vehicle.fuel_type}")
                print(f"{len(self.vehicles) + 1}. Add New Vehicle")
                print("0. Exit")


    def view_summary(self):
        """Print a human-readable summary of recorded trips and totals."""

        for trip in self.trips:
            print(f"Trip from {trip.route.origin} to {trip.route.destination}: {trip.total_emissions} lbs CO2")

        weekly_emissions = round(sum(trip.total_emissions*(trip.occurrence / trip.frequency)*7 for trip in self.trips), 2)
        monthly_emissions = round(sum(trip.total_emissions*(trip.occurrence / trip.frequency)*30 for trip in self.trips), 2)
        yearly_emissions = round(sum(trip.total_emissions*(trip.occurrence / trip.frequency)*365 for trip in self.trips), 2)

        print(f"Weekly Emissions: {weekly_emissions} lbs CO2")
        print(f"Monthly Emissions: {monthly_emissions} lbs CO2")
        print(f"Yearly Emissions: {yearly_emissions} lbs CO2")

    def save_data(self):
        """Persist the current application state to a JSON file.

        This method prompts the user for a filename (default
        `data/savefile.json`) and writes a JSON object containing
        the application's vehicles and trips. Vehicles are written
        using `Vehicle.to_dict()`. Trips are serialized with their
        route (origin, destination, distance), frequency, occurrence,
        passengers, and a reference to the vehicle either by index
        (`vehicle_index`) or embedded vehicle dictionary (`vehicle`).

        The method ensures the containing directory exists and prints
        a short confirmation message after successful write.
        """
        filename = input("Enter filename to save to (default: data/savefile.json): ").strip()
        if filename == "":
            filename = "data/savefile.json"

        # Ensure directory exists
        dirpath = os.path.dirname(filename)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)

        payload = {
            "vehicles": [v.to_dict() for v in self.vehicles],
            "trips": []
        }

        for trip in self.trips:
            # reference vehicle by index in vehicles list if present, else save full vehicle dict
            try:
                vehicle_index = self.vehicles.index(trip.vehicle)
            except ValueError:
                vehicle_index = None

            trip_record = {
                "route": {
                    "origin": trip.route.origin,
                    "destination": trip.route.destination,
                    "distance": trip.route.distance
                },
                "frequency": trip.frequency,
                "occurrence": trip.occurrence,
                "passengers": trip.passengers,
                "vehicle_index": vehicle_index,
                "vehicle": trip.vehicle.to_dict() if vehicle_index is None else None
            }
            payload["trips"].append(trip_record)

        with open(filename, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)

        print(f"Data saved to {filename}")

    def load_file(self):
        """Load application state from a JSON save file.

        This method prompts the user for a filename (default
        `data/savefile.json`), reads the file, and reconstructs the
        in-memory `vehicles` and `trips` lists. Vehicles are rebuilt
        using `Vehicle.from_dict()` when possible; trips are
        reconstructed by creating `Route` objects and pairing them
        with their associated `Vehicle` instances (by index or by
        embedded vehicle data).

        After loading, `self.vehicles` and `self.trips` are replaced
        with the contents of the file. A short summary is printed
        describing how many records were loaded.
        """
        filename = input("Enter filename to load from (default: data/savefile.json): ").strip()
        if filename == "":
            filename = "data/savefile.json"

        if not os.path.exists(filename):
            print(f"File {filename} does not exist.")
            return

        with open(filename, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        # Rebuild vehicles
        self.vehicles = []
        for vdata in data.get("vehicles", []):
            try:
                vehicle = Vehicle.from_dict(vdata)
            except Exception:
                # Fallback: construct directly
                vehicle = Vehicle(vdata.get("make"), vdata.get("model"), vdata.get("year"))
            self.vehicles.append(vehicle)

        # Rebuild trips
        self.trips = []
        for trec in data.get("trips", []):
            r = trec.get("route", {})
            route = Route(r.get("origin", ""), r.get("destination", ""), r.get("distance", 0))

            vehicle = None
            vindex = trec.get("vehicle_index")
            if vindex is not None and 0 <= vindex < len(self.vehicles):
                vehicle = self.vehicles[vindex]
            else:
                vdata = trec.get("vehicle")
                if vdata:
                    try:
                        vehicle = Vehicle.from_dict(vdata)
                    except Exception:
                        vehicle = Vehicle(vdata.get("make"), vdata.get("model"), vdata.get("year"))

            if vehicle is None:
                print("Skipping trip with missing vehicle data.")
                continue

            frequency = trec.get("frequency", 0)
            occurrence = trec.get("occurrence", 1)
            passengers = trec.get("passengers", 1)

            trip = Trip(route, vehicle, frequency, occurrence, passengers)
            self.trips.append(trip)

        print(f"Loaded {len(self.vehicles)} vehicles and {len(self.trips)} trips from {filename}")