import firebase_admin as fa


def db_init():
    """ Log in creds"""
    # Firebase credentials
    file_json = "jobtrack-39d73-firebase-adminsdk-wpmtz-1bb461d761.json"
    cred = fa.credentials.Certificate("./private/" + file_json)
    fa.initialize_app(cred)
