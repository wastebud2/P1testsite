from flask import Flask, render_template, redirect, request
from app.brute_force import sortLocations
import json
import firebase_admin
from firebase_admin import credentials, firestore



## Setup ##
app = Flask(__name__)
cred = credentials.Certificate("firebase_service_key.json")
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
units_ref = db.collection('enheder')


## Routes ##
@app.route("/")
def index():
    # Sort by type, so 'Plast og Metal' de ligger i deres kategorier
    data = units_ref.order_by('type').order_by('fill', direction=firestore.Query.DESCENDING)
    return render_template('index.html', entries=data.stream())

@app.route("/sort/<float:fill>")
def sort(fill):
    locs = []
    for entry in units_ref.stream():
        entry_dict = entry.to_dict()
        if entry_dict['fill'] > fill:
            new_entry = [entry.id, entry_dict["lat"], entry_dict["lng"]]
            locs.append(new_entry)
    bestOrder = sortLocations(locs)
    locs = locs[::-1] # flip list order
    locs = [locs[i] for i in bestOrder]
    return json.dumps(locs)

@app.route("/sort/<string:type>/<float:fill>")
def sort_with_type(type, fill):
    locs = []
    for entry in units_ref.stream():
        entry_dict = entry.to_dict()
        if entry_dict['type'] == type and entry_dict['fill'] > fill:
            new_entry = [entry.id, entry_dict["lat"], entry_dict["lng"]]
            locs.append(new_entry)
    bestOrder = sortLocations(locs)
    locs = locs[::-1] # flip list order
    locs = [locs[i] for i in bestOrder]
    return json.dumps(locs)

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

#HEJ