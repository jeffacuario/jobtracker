import firebase_admin as fa
from firebase_admin import firestore
import json
import pyrebase
from flask import session
import os
import base64


def b64d(s):
    return base64.b64decode(s).decode()


def db_init():
    """ Log in creds"""
    # Firebase credentials
    file_json = "credentials.json"
    try:
        cred = fa.credentials.Certificate("./private/" + file_json)
    except IOError:
        private_key = b64d(os.getenv('PRIVATE_KEY'))
        firebase_credentials = {
            "type": "service_account",
            "project_id": os.getenv('PROJECT_ID'),
            "private_key_id": os.getenv('PRIVATE_KEY_ID'),
            "private_key": private_key,
            "client_email": os.getenv('CLIENT_EMAIL'),
            "client_id": os.getenv('CLIENT_ID'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL')
        }
        cred = fa.credentials.Certificate(firebase_credentials)
    fa.initialize_app(cred)


def fbStorage_init():
    """ Initialize the connection to firebase storage"""
    # pyrebase credentials
    with open("./private/jobtrack-pyrebase-credentials.json") as json_file:
        pyrebase_config = json.load(json_file)
    return pyrebase.initialize_app(pyrebase_config)


def dbConn(collection):
    """Takes a collection and connects to firestore.Returns the collection"""
    return firestore.client().collection(collection)


def allDocs(col, userID):
    """Takes a collection and userID and returns list of the User's documents"""
    all_docs = []
    for doc in col.stream():
        x = doc.to_dict()
        if userID == x['userID']:
            x['id'] = doc.id
            all_docs.append(x)
    return all_docs


def getJobs(userID):
    """Returns all user jobs"""
    return allDocs(dbConn('applications'), userID)


def addJob(val):
    """Adds job to firebase applications collection"""
    values = json.dumps(val.__dict__)
    dbConn('applications').add(eval(values))
    return "success"


def deleteJob(jobID, userID):
    """Deletes provided jobID from the firebase database"""
    dbConn('applications').document(jobID).delete()
    for item in getSkills(userID):
        if item['posID'] == jobID:
            deleteSkill(item['id'])
    return 'deleted'


def updateJob(jobID, data, userID):
    """Updates provided jobID from the firebase database"""
    before = dbConn('applications').document(jobID).get().to_dict()
    dbConn('applications').document(jobID).update(data)

    # handle change in position, company, or type
    if before['position'] != data['position'] or before['company'] != data['company'] or before['type'] != data['type']:
        for item in getSkills(userID):
            if item['posID'] == jobID:
                dbConn('skills').document(item['id']).update(
                    {
                        'position': data['position'],
                        'company': data['company'],
                        'type': data['type']
                    }
                )
    return 'updated'


def getSkills(userID):
    """Returns all user skills"""
    return allDocs(dbConn('skills'), userID)


def addSkill(val):
    """Adds skill to firebase skills collection"""
    values = json.dumps(val.__dict__)
    dbConn('skills').add(eval(values))
    return "success"


def deleteSkill(skillID):
    """Deletes provided skillID from the firebase database"""
    dbConn('skills').document(skillID).delete()
    return 'deleted'


def updateSkill(skillID, data):
    """Updates provided skillID from the firebase database"""
    values = json.dumps(data.__dict__)
    dbConn('skills').document(skillID).update(eval(values))
    return 'updated'


def getContacts(userID):
    """Returns all user contacts"""
    return allDocs(dbConn('contacts'), userID)


def addContact(val):
    """Adds contact to firebase contacts collection"""
    values = json.dumps(val.__dict__)
    dbConn('contacts').add(eval(values))
    return "success"


def deleteContact(contactID):
    """Deletes provided contactID from the firebase database"""
    dbConn('contacts').document(contactID).delete()
    return 'deleted'


def updateContact(contactID, data):
    """Updates provided contactID from the firebase database"""
    values = json.dumps(data.__dict__)
    dbConn('contacts').document(contactID).update(eval(values))
    return 'updated'


def addContactImage(img, userID):
    """Adds the contact image to firebase storage"""
    try:
        path_on_cloud = "contact_images/" + userID + "/" + img.filename
        upload = fbStorage_init().storage().child(path_on_cloud).put(img, session.get("token_id"))
        image_url = fbStorage_init().storage().child(path_on_cloud).get_url(upload["downloadTokens"])
        return image_url

    except Exception as e:
        print('error uploading contact photo: ', e)


def getContactImgURL(contactID):
    """Get the Contact entry values so we can extract IMG URL"""
    x = dbConn('contacts').document(contactID).get()
    return x.to_dict()


def retrieve_all():
    """ Retrieve all the user data"""
    # Get data per the user - however, currently, this is a mock
    db = firestore.client()

    applications = db.collection('applications').get()
    skills = db.collection("skills").get()
    contacts = db.collection("contacts").get()

    app_list = [app for app in applications]
    skills_list = [skill for skill in skills]
    contact_list = [contact for contact in contacts]

    data = {
        "applications": app_list,
        "skills": skills_list,
        "contacts": contact_list
    }
    return data
