from firebase_admin import auth as fa_auth
from distutils.command.config import config  # noqa F401
from flask import Blueprint, render_template, request, redirect, url_for, g, session  # noqa E501
import json
import pyrebase
import requests
import functools
import os


auth = Blueprint('auth', __name__)

"""
    Initialize pyrebase app
"""
try:
    with open('./private/jobtrack-pyrebase-credentials.json') as json_file:
        pyrebase_config = json.load(json_file)
except IOError:
    pyrebase_config = {
        "apiKey": os.getenv('APIKEY'),
        "authDomain": os.getenv('AUTHDOMAIN'),
        "databaseURL": os.getenv('DATABASEURL'),
        "storageBucket": os.getenv('STORAGEBUCKET')
    }
firebase = pyrebase.initialize_app(pyrebase_config)
fb_auth = firebase.auth()


@auth.route('/login', methods=['POST', 'GET'])
def login():
    """
    Render Login Page
    """
    if request.method == 'POST':
        username = request.form['inputEmail']
        password = request.form['inputPassword']

        error_message = None

        try:
            user = fb_auth.sign_in_with_email_and_password(username, password)
            # print(user)
            session.clear()
            session['user_id'] = user['localId']
            session['token_id'] = user['idToken']
            return redirect(url_for('views.jobs'))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            # print(error)
            if error == 'INVALID_PASSWORD' or error == 'EMAIL_NOT_FOUND':
                error_message = "You have entered an invalid email or password"
            return render_template("auth/login.html", error_message=error_message)  # noqa E501
    return render_template("auth/login.html")


@auth.route('/register', methods=['POST', 'GET'])
def register():
    """
    Render Register Page
    """
    if request.method == 'POST':
        username = request.form['inputName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        error_message = None

        try:
            user = fb_auth.create_user_with_email_and_password(email, password)
            fa_auth.update_user(user.get("localId"), display_name=username)
        except requests.exceptions.HTTPError as e:
            # print(e)
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            # print(error)
            if error == 'EMAIL_EXISTS':
                error_message = "Email already registered"
            elif error == 'WEAK_PASSWORD : Password should be at least 6 characters':  # noqa E501
                error_message = "Password should be at least 6 characters"
            return render_template("auth/register.html",
                                   error_message=error_message)
        else:
            return redirect(url_for("auth.login"))

    return render_template('auth/register.html')


@auth.route('/reset', methods=['POST', 'GET'])
def reset():
    """
    Password Reset Page
    """
    if request.method == 'POST':
        email = request.form['inputEmail']
        try:
            fb_auth.send_password_reset_email(email)
            return redirect(url_for("auth.login"))
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == 'EMAIL_NOT_FOUND':
                error_message = "Email not found"
            return render_template("auth/reset.html", error_message=error_message)  # noqa E501
    return render_template('auth/reset.html')


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    token_id = session.get('token_id')

    if user_id is None:
        g.user = None
    else:
        try:
            g.user = fb_auth.get_account_info(token_id)
            # print(g.user)
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            # print(error)
            if error == 'INVALID_ID_TOKEN':
                session.clear()
                return redirect(url_for("auth.logout"))


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.jobs'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
