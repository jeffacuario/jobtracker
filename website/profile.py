from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, \
    session, send_file
import requests
import json
import pyrebase
from firebase_admin import auth as fa_auth
import os

auth = Blueprint("auth", __name__)
profile = Blueprint("profile", __name__)

with open("./private/jobtrack-pyrebase-credentials.json") as json_file:
    pyrebase_config = json.load(json_file)
firebase = pyrebase.initialize_app(pyrebase_config)

# storage
fb_storage = firebase.storage()

# auth
fb_auth = firebase.auth()

# reference: https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "webp"])

path_local = "website/static/images/profile/"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in \
        ALLOWED_EXTENSIONS


@profile.route("/settings")
def settings_page():
    return render_template("settings/settings.html")


@profile.route("/settings", methods=["POST"])
def update_file():
    if "file" in request.files:
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path_local + filename)
            user_uid = session.get("user_id")
            path_on_cloud = "profile_images/" + user_uid + "/" + filename
            upload = fb_storage.child(path_on_cloud).put(
                path_local + filename, session.get("token_id")
            )
            image_url = fb_storage.child(path_on_cloud).get_url(
                upload["downloadTokens"]
            )
            fa_auth.update_user(session.get("user_id"), photo_url=image_url)
            if os.path.exists(path_local + filename):
                os.remove(path_local + filename)
        return redirect(url_for("profile.settings_page"))
    if "inputEmail" in request.form:
        email = request.form["inputEmail"]
        fa_auth.update_user(session.get("user_id"), email=email)
        return redirect(url_for("auth.login"))
    if "inputPassword" in request.form:
        password = request.form["inputPassword"]
        fa_auth.update_user(session.get("user_id"), password=password)
        return redirect(url_for("auth.login"))


@profile.route("/display")
def display_default():
    default_url = "https://firebasestorage.googleapis.com/v0/b/jobtrack-39d73.appspot.com/o/photo_icon.jpeg?alt=media&token=e1c9c533-0aa1-44bb-b465-762fd9d1b928"
    r = requests.get(default_url, stream=True)
    res = r.raw
    return send_file(res, mimetype='image/jpeg')

