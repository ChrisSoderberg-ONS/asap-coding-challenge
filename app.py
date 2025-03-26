from flask import Flask, render_template, request
from mapping.folium_map import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/slider_update", methods=["POST"])
def slider():
    received_data = request.data
    return received_data