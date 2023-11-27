import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin import firestore
import os
import requests
# Use the application default credentials
from datetime import datetime, date
import time


db = None

try:
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
except:
    raise Exception("add GOOGLE_APPLICATION_CREDENTIALS to env")


def initialize_firebase():
    global db

    json_path = os.path.join(GOOGLE_APPLICATION_CREDENTIALS)

    cred = credentials.Certificate(json_path)
    firebase_admin.initialize_app(cred)

    db = firestore.client()


def get_config():
    scrpt_ref = db.collection(u'').document(u'config')
    doc = scrpt_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        print(u'No such document!')

    return None


def stamp(dictionary):
    data = dictionary

    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
    data["timestamp"] = timestamp

    current_time = time.time()
    doc_ref = db.collection(u'fblr-scrpt').document(u'executions').collection(u'records').document(u'{}'.format(current_time))
    doc_ref.set(data, merge=True)
