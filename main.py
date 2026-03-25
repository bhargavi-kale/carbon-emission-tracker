from flask import Flask, render_template, request
from src.route import Route
from src.trip import Trip
from src.vehicle import Vehicle

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html") #flaskstuff






if __name__ == "__main__":
    app.run(debug=True)