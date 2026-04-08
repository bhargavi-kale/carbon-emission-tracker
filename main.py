"""
Main application module for the Carbom Commute System.
Handles routing for vehicle data and integration with Google Maps API.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash

from models import db, VehicleModel

# from src.route import Route
# from src.trip import Trip
from src.vehicle import Vehicle

# Load environment variables
load_dotenv()


def create_app():
    """create and configure the Flask application."""
    flask_app = Flask(__name__)

    # Configuration - adjust path as needed
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carbon_commute.db"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.secret_key = "your_secret_key"

    # 1. Link the db instance to this specific app
    db.init_app(flask_app)

    # 2. Create the tables (Edge case: this must happen inside a context)
    with flask_app.app_context():
        db.create_all()

    return flask_app

app = create_app()

# Load dataset
df = pd.read_csv("data/vehicles.csv", low_memory=False)


@app.route("/")
def home():
    """Render the home page with the Google Maps API key."""
    vehicles = VehicleModel.query.all()  # Get all vehicles from DB
    api_key = os.getenv("GOOGLE_API_KEY")
    return render_template("home.html", API_KEY=api_key, vehicles=vehicles)

@app.route("/calculate", methods=["POST"])
def calculate():
    """Handle form submission to calculate emissions for a commute."""
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    passengers = int(request.form.get("passengers", 1))
    vehicle_id = int(request.form.get("vehicle_id"))

    vehicle = VehicleModel.query.get(vehicle_id)

    # --- Find vehicle in CSV dataset ---
    match = df[
        (df["make"] == vehicle.make) &
        (df["model"] == vehicle.model) &
        (df["year"] == vehicle.year)
    ]

    # Default fuel type
    fuel_type = "Gasoline"

    if not match.empty:
        fuel_type = match.iloc[0]["fuelType"]

    # --- Emission factors ---
    emission_factors = {
        "Gasoline": 0.20,
        "Diesel": 0.18,
        "Hybrid": 0.12,
        "Electric": 0.05
    }

    factor = emission_factors.get(fuel_type, 0.20)

    # Example distance (later from Google Maps API)
    distance_km = 10.5

    # --- Emissions calculation ---
    total_emissions = distance_km * factor
    emissions_per_person = total_emissions / passengers

    calculation = {
        "vehicle": vehicle,
        "fuel_type": fuel_type,
        "origin": origin,
        "destination": destination,
        "distance": distance_km,
        "passengers": passengers,
        "total_emissions": round(total_emissions, 2),
        "emissions_per_person": round(emissions_per_person, 2),
    }

    api_key = os.getenv("GOOGLE_API_KEY")
    vehicles = VehicleModel.query.all()

    return render_template(
        "home.html",
        API_KEY=api_key,
        vehicles=vehicles,
        calculation=calculation
    )

@app.route("/add-vehicle")
def add_vehicle():
    """Render the vehicle selection page with sorted manufacturer list."""
    makes = sorted(df["make"].unique().tolist())
    return render_template("vehicle.html", makes=makes)


@app.route("/save-vehicle", methods=["POST"])
def save_vehicle():
    """Handle form submission to save a new vehicle for the user."""
    make = request.form.get("make")
    model = request.form.get("model")
    year = int(request.form.get("year"))

    # Check if this exact vehicle already exists in the database
    existing_vehicle = VehicleModel.query.filter_by(
        make=make, model=model, year=year
    ).first()
    print(existing_vehicle, "existing vehicle")

    if existing_vehicle:
        # Inform the user it's already there
        print("existing vehicle here")
        flash(f"Note: {make} {model} ({year}) is already in your list!", "info")
        return redirect(url_for("home"))
    economy_data = Vehicle.fetch_economy_data(make, model, year)
    # If it doesn't exist, proceed with saving
    try:
        new_vehicle = VehicleModel(make=make, model=model, year=year,
                              economy_id=int(economy_data["id"]),
                              fuel_type=economy_data["fuelType1"],
                              combined_mpg=float(economy_data["comb08"]))
        db.session.add(new_vehicle)
        db.session.commit()
        print(new_vehicle, "new vehicle")
        flash(f"Success! {make} {model} added.", "success")
    except Exception as e:
        print("Error saving vehicle:", e)
        db.session.rollback()
        flash("An error occurred while saving.", "danger")

    return redirect(url_for("home"))


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


@app.route("/api/vehicles")
def get_vehicles():
    """API endpoint to retrieve all vehicles in the database as JSON."""
    all_vehicles = VehicleModel.query.all()

    # Convert the database objects into a list of dictionaries
    vehicles_list = []
    for vehicle in all_vehicles:
        vehicles_list.append(
            {
                "id": vehicle.id,
                "make": vehicle.make,
                "model": vehicle.model,
                # 'fuel_type': vehicle.fuel_type,
                # 'efficiency': vehicle.efficiency  # grams of CO2 per mile/km
            }
        )

    # jsonify converts the list into a JSON response
    return jsonify(vehicles_list)



if __name__ == "__main__":
    app.run(debug=True)
