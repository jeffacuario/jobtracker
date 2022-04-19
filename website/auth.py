from distutils.command.config import config
from flask import Blueprint, render_template, request, redirect, url_for
import json, pyrebase, requests


auth = Blueprint('auth', __name__)

"""
    Initialize pyrebase app
"""
with open('./private/jobtrack-pyrebase-credentials.json') as json_file:
        config = json.load(json_file)
firebase = pyrebase.initialize_app(config)
fb_auth = firebase.auth()


@auth.route('/login')
def login():
    """
    Render Login Page
    """
    return render_template("auth/login.html")


@auth.route('/register', methods=['POST', 'GET'])
def register():
    """
    Render Register Page
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        error_message = None

        try:
            fb_auth.create_user_with_email_and_password(username, password)
        except requests.exceptions.HTTPError as e: # we will need to handle the exception and display error to user
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            print(error)
            if error == 'EMAIL_EXISTS':
                error_message = "Email already registered"
            elif error == 'WEAK_PASSWORD : Password should be at least 6 characters':
                error_message = "Password should be at least 6 characters"
            return render_template("auth/register.html", error_message=error_message)
        else:
            return redirect(url_for("auth.login"))

    return render_template('auth/register.html')

