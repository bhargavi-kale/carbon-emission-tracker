import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
from src.route import Route
from src.trip import Trip
from src.vehicle import Vehicle

app = Flask(__name__)

@app.route("/")
def home():
    API_KEY = os.getenv("GOOGLE_API_KEY")
    return render_template("index.html", API_KEY=API_KEY) #flaskstuff






if __name__ == "__main__":
    app.run(debug=True)