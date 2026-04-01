"""
Main application module for the Carbom Commute System.
Handles routing for vehicle data and integration with Google Maps API.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify

from src.route import Route
from src.trip import Trip
from src.vehicle import Vehicle

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data/vehicles.csv", low_memory=False)

@app.route("/")
def home():
    """Render the home page with the Google Maps API key.""" 
    api_key = os.getenv("GOOGLE_API_KEY") 
    return render_template("home.html", API_KEY=api_key)


@app.route("/add-vehicle")
def add_vehicle():
    """Render the vehicle selection page with sorted manufacturer list."""
    makes = sorted(df["make"].unique().tolist())
    return render_template("vehicle.html", makes=makes)


@app.route("/get_models/<make>")
def get_models(make):
    """Return a JSON list of unique models for a given manufacturer."""
    models = sorted(df[df["make"] == make]["model"].unique().tolist())
    return jsonify(models)


@app.route("/get_years/<make>/<model>")
def get_years(make, model):
    """Return a JSON list of available years for a specific make and model."""
    years = sorted(
        df[(df["make"] == make) & (df["model"] == model)]["year"].unique().tolist(),
        reverse=True,
    )
    return jsonify([int(y) for y in years])


if __name__ == "__main__":
   app.run(debug=True)