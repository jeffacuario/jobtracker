import firebase_admin as fa


def db_init():
    """ Log in creds"""
    # Firebase credentials
    file_json = "credentials.json”"
    cred = fa.credentials.Certificate("./private/" + file_json)
    fa.initialize_app(cred)
