import firebase_admin as fa
from firebase_admin import firestore
import json


def db_init():
    """ Log in creds"""
    # Firebase credentials
    file_json = "credentials.json"
    cred = fa.credentials.Certificate("./private/" + file_json)
    fa.initialize_app(cred)


def dbConn(collection):
    """Takes a collection and connects to firestore.Returns the collection"""
    return firestore.client().collection(collection)


def allDocs(col):
    """Takes a collection and returns list of dictionary"""
    all_docs = []
    for doc in col.stream():
        x = doc.to_dict()
        x['id'] = doc.id
        all_docs.append(x)
    return all_docs


def getJobs():
    """Returns all jobs"""
    return allDocs(dbConn('applications'))


def addJob(val):
    """Adds job to firebase applications collection"""
    values = json.dumps(val.__dict__)
    dbConn('applications').add(eval(values))
    return "success"


def deleteJob(jobID):
    """Deletes provided jobID from the firebase database"""
    dbConn('applications').document(jobID).delete()
    return 'deleted'


def getSkills():
    """Returns all skills"""
    return allDocs(dbConn('skills'))


def addSkill(val):
    """Adds skill to firebase skills collection"""
    values = json.dumps(val.__dict__)
    dbConn('skills').add(eval(values))
    return "success"


def deleteSkill(skillID):
    """Deletes provided skillID from the firebase database"""
    dbConn('skills').document(skillID).delete()
    return 'deleted'
