import firebase_admin as fa
from firebase_admin import firestore
import json


def db_init():
    """ Log in creds"""
    # Firebase credentials
    file_json = "credentials.json"
    cred = fa.credentials.Certificate("./private/" + file_json)
    fa.initialize_app(cred)


def getJobs():
    db = firestore.client()
    applications = db.collection('applications')

    all_jobs = []
    for doc in applications.stream():
        x = doc.to_dict()
        x['id'] = doc.id
        all_jobs.append(x)

    return all_jobs


def addJob(val):
    values = json.dumps(val.__dict__)
    db = firestore.client()
    db.collection('applications').add(eval(values))
    return "success"
