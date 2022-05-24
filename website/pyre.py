from flask import Blueprint
import json
import pyrebase

pyre = Blueprint('pyre', __name__)

# initialize pyrebase
try:
    with open('./private/jobtrack-pyrebase-credentials.json') as json_file:
        pyrebase_config = json.load(json_file)
    firebase = pyrebase.initialize_app(pyrebase_config)

    fb_auth = firebase.auth()
    fb_storage = firebase.storage()
except (IOError, OSError, ImportError) as e:
    print(e)
