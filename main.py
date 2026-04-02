"""
Main application module for the Carbom Commute System.
Handles routing for vehicle data and integration with Google Maps API.
"""

import os
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash

from models import db, Vehicle

# from src.route import Route
# from src.trip import Trip
# from src.vehicle import Vehicle

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
    vehicles = Vehicle.query.all()  # Get all vehicles from DB
    api_key = os.getenv("GOOGLE_API_KEY")
    return render_template("home.html", API_KEY=api_key, vehicles=vehicles)

@app.route("/calculate", methods=["POST"])
def calculate():
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    passengers = int(request.form.get("passengers", 1))

    vehicle_id_str = request.form.get("vehicle_id")
    if not vehicle_id_str:
        flash("Please select a vehicle before calculating emissions.", "warning")
        return redirect(url_for("home"))

    try:
        vehicle_id = int(vehicle_id_str)
    except (ValueError, TypeError):
        flash("Invalid vehicle selection.", "danger")
        return redirect(url_for("home"))

    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        flash("Selected vehicle not found. Please add or choose a valid vehicle.", "warning")
        return redirect(url_for("home"))

    # Example: calculate distance (you can integrate with Google Maps API)
    distance_km = 10.5  # Replace with actual calculation
    # Example CO2: let's say 0.2 kg per km per passenger
    emissions = distance_km * 0.2 * passengers

    calculation = {
        "vehicle": vehicle,
        "origin": origin,
        "destination": destination,
        "distance": distance_km,
        "passengers": passengers,
        "emissions": round(emissions, 2),
    }

    api_key = os.getenv("GOOGLE_API_KEY")
    vehicles = Vehicle.query.all()  # Needed for the dropdown

    return render_template("home.html", API_KEY=api_key, vehicles=vehicles, calculation=calculation)


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
    existing_vehicle = Vehicle.query.filter_by(
        make=make, model=model, year=year
    ).first()
    print(existing_vehicle, "existing vehicle")

    if existing_vehicle:
        # Inform the user it's already there
        print("existing vehicle here")
        flash(f"Note: {make} {model} ({year}) is already in your list!", "info")
        return redirect(url_for("home"))

    # If it doesn't exist, proceed with saving
    try:
        new_vehicle = Vehicle(make=make, model=model, year=year)
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
    all_vehicles = Vehicle.query.all()

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
