## Imports ##
from flask import Flask, render_template, redirect, request, flash
from app.brute_force import sortLocations # Brute force algorithm
from app.ACO import sort_ACO # Ant Colony algorithm
import json
import firebase_admin
from firebase_admin import credentials, firestore



## Setup ##
app = Flask(__name__) # Launch flask-app
cred = credentials.Certificate("firebase_service_key.json") # Get Firebase credentials from json-file
firebase = firebase_admin.initialize_app(cred) # Get admin-access to Firebase
db = firestore.client() # Access Firebase Firestore
units_ref = db.collection('enheder') # Get collection of documents from database

aaf = ["Aalborg Forsyning", 57.026012, 9.921496] # Coordinates for AAF, the starting location of all garbage trucks

## Routes ##
# Default route and index-site
@app.route("/")
def index():
    # Sort entries by type and fill amount
    data = units_ref.order_by('type').order_by('fill', direction=firestore.Query.DESCENDING)
    return render_template('index.html', entries=data.stream())

# Optimize route based only on fill amount
@app.route("/sort/<float:fill>")
def sort(fill):
    locs = []
    locs.append(aaf)
    for entry in units_ref.stream():
        entry_dict = entry.to_dict()
        if entry_dict['fill'] > fill:
            new_entry = [entry.id, entry_dict["lat"], entry_dict["lng"]]
            locs.append(new_entry)
    locs = sort_ACO(locs)
    return json.dumps(locs)

# Optimize route based on fill amount and trash type
@app.route("/sort/<string:type>/<float:fill>")
def sort_with_type(type, fill):
    locs = []
    locs.append(aaf) # Add start location to location list
    for entry in units_ref.stream(): # For every entry in units_ref collection
        entry_dict = entry.to_dict() # Get entry as datatype dict
        # If entry type is equal to given type, and fill amount is over given fill amount ...
        if entry_dict['type'] == type and entry_dict['fill'] > fill:
            # ... get id, latitude and longitude of entry, and add to new variable (new_entry)
            new_entry = [entry.id, entry_dict["lat"], entry_dict["lng"]]
            locs.append(new_entry) # Add new_entry to location list
    locs = sort_ACO(locs) # Sort location list via ACO algorithm
    return json.dumps(locs) # Return sorted list as json-array

@app.route("/sort/GUI", methods=['POST'])
def sort_GUI():
    if request.method == 'POST':
        type = request.form['typeSelect']
        fill = float(request.form['fillRange'])
        if type == 'NoFilter':
            return sort(fill)
        else:
            return sort_with_type(type, fill)


if __name__ == "__main__":
    app.run(debug=True)
