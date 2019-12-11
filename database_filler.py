import firebase_admin
from firebase_admin import credentials, firestore
import random

# SETUP
cred = credentials.Certificate("firebase_service_key.json")
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
units_ref = db.collection('enheder')

types = ["Plast", "Mad", "Pap", "Rest"]


for i in range(0, 20):
    data = {
        u'fill': random.randint(0,100),
        u'lat': random.randint(0,100),
        u'lng': random.randint(0,100),
        u'type': types[random.randint(0,3)]
    }
    units_ref.document(u'Test{0}'.format(i)).set(data)