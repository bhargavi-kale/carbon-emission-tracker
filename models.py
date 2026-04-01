"""
models.py – SQLAlchemy db instance and models for the carbon commute application.
Developer:  Bella, Bhargavi
"""

from flask_sqlalchemy import SQLAlchemy

# ---------------------------------------------------------------------------
# Extension instance – shared across the application
# ---------------------------------------------------------------------------

db = SQLAlchemy()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class Vehicle(db.Model):
    """ORM model representing a vehicle.

    :ivar id: Primary key.
    :ivar make: Vehicle manufacturer, e.g., "Toyota".
    :ivar model: Vehicle model name, e.g., "Camry".
    :ivar year: Vehicle's model year, e.g., 2020.
    """

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def to_dict(self) -> dict:
        """Convert the Vehicle object into a dictionary."""
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
        }


class Route(db.Model):
    """ORM model representing a route between two locations.

    :ivar id: Primary key.
    :ivar origin: Starting location of the route.
    :ivar destination: Ending location of the route.
    :ivar distance: Total distance of the route (in kilometers).
    """

    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, default=0.0, nullable=False)

    def to_dict(self) -> dict:
        """Convert the Route object into a dictionary."""
        return {
            "id": self.id,
            "origin": self.origin,
            "destination": self.destination,
            "distance": self.distance,
        }


class Trip(db.Model):
    """ORM model representing a trip taken with a vehicle along a route.

    :ivar id: Primary key.
    :ivar route_id: Foreign key to the Route table.
    :ivar vehicle_id: Foreign key to the Vehicle table.
    :ivar frequency: Frequency period in days.
    :ivar occurrence: Number of occurrences within the frequency.
    :ivar passengers: Number of passengers for the trip.
    """

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    frequency = db.Column(db.Integer, default=0, nullable=False)
    occurrence = db.Column(db.Integer, default=1, nullable=False)
    passengers = db.Column(db.Integer, default=1, nullable=False)

    route = db.relationship("Route", backref=db.backref("trips", lazy=True))
    vehicle = db.relationship("Vehicle", backref=db.backref("trips", lazy=True))

    def to_dict(self) -> dict:
        """Convert the Trip object into a dictionary, including related Route and Vehicle data."""
        return {
            "id": self.id,
            "route": self.route.to_dict() if self.route else None,
            "vehicle": self.vehicle.to_dict() if self.vehicle else None,
            "frequency": self.frequency,
            "occurrence": self.occurrence,
            "passengers": self.passengers,
        }
