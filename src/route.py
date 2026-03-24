"""Route model and utilities.

This module defines the :class:`Route` object which contains simple
origin/destination information and a placeholder method for fetching
route metrics such as distance. The real implementation should call
an external routing API (for example, Google Routes API) to populate
the distance and other route metadata.
"""
try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv():
        return None
import os
import requests
import json


class Route:
    """Represent a travel route between an origin and a destination.

    Parameters
    ----------
    origin : str
        The starting address or location identifier for the route.
    destination : str
        The destination address or location identifier for the route.
    total_distance : float, optional
        Pre-populated distance for the route in miles (default is 0).
    """

    def __init__(self, origin, destination, total_distance=0):
        self.origin = origin
        self.destination = destination
        self.distance = total_distance

    def fetch_route_data(self):
        """Fetch route metrics and update this Route instance.

        Returns
        -------
        float
            The distance for the route in miles.
        """
        # Placeholder for HTTP request to Google Route Matrix API
        #if self.distance == 0:
        #    self.distance = 100  # Placeholder distance in miles to prevent failure, replace this with API
        #return self.distance
        load_dotenv()

        API_KEY = os.getenv("GOOGLE_API_KEY") # DO NOT PUSH THIS TO PUBLIC REPO
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
        }

        body = {
            "origin": {
                "address": self.origin
            },
            "destination": {
                "address": self.destination
            },
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE",
            "computeAlternativeRoutes": False,
            "routeModifiers": {
                "avoidTolls": False,
                "avoidHighways": False,
                "avoidFerries": False
            },
            "languageCode": "en-US",
            "units": "METRIC"
        }

        response = requests.post(url, headers=headers, data=json.dumps(body))

        data = response.json()
        distance_meters = data["routes"][0]["distanceMeters"]
        self.distance = self.meters_to_miles(distance_meters)
        return self.distance

    def meters_to_miles(self, meters: float) -> float:
        """Convert meters to miles.

        Parameters
        ----------
        meters : float
            Distance in meters.

        Returns
        -------
        float
            Distance in miles.
        """
        return meters * 0.000621371
