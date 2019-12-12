import firebase_admin
from firebase_admin import credentials, firestore
import random

# SETUP
cred = credentials.Certificate("firebase_service_key.json")
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
units_ref = db.collection('enheder')

types = ["Plast", "Mad", "Pap", "Rest"]

vejnavn1 = ["Danmarks", "Vej", "Grønlands", "Asyl", "Hadsund", "Blegkilde", "Badehus", "Sø"]
vejnavn2 = ["gade", "vej", "gaard", " Allé", "stræde", " Brygge"]


for i in range(0, 20):
    data = {
        u'fill': random.randint(0,100),
        u'address': "{0}{1} {2}".format(vejnavn1[random.randint(0,len(vejnavn1)-1)], vejnavn2[random.randint(0,len(vejnavn2)-1)], random.randint(1,50)),
        u'lat': random.uniform(57.026536, 57.037774),
        u'lng': random.uniform(9.892192,9.929614),
        u'type': types[random.randint(0,3)]
    }
    units_ref.document(u't{0}'.format(i)).set(data)