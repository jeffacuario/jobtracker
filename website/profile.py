from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash,session
import json
import pyrebase
from firebase_admin import auth as fa_auth

auth = Blueprint('auth', __name__)
profile = Blueprint("profile", __name__)

with open("./private/jobtrack-pyrebase-credentials.json") as json_file:
    pyrebase_config = json.load(json_file)
firebase = pyrebase.initialize_app(pyrebase_config)

# storage
fb_storage = firebase.storage()

# auth
fb_auth = firebase.auth()

#reference: https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@profile.route('/settings')
def settings_page():
	return render_template('settings/settings.html')

@profile.route("/settings", methods=["POST"])
def update_file():
    if "file" in request.files:
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_uid = session.get("user_id")
            path_on_cloud = "profile_images/" + user_uid + "/"+filename
            upload = fb_storage.child(path_on_cloud).put("website/static/images/"+filename,session.get("token_id"))
            image_url = fb_storage.child(path_on_cloud).get_url(upload['downloadTokens'])
            fa_auth.update_user(session.get("user_id"), photo_url=image_url)
            return render_template("settings/settings.html", filename=filename)
    if 'inputEmail' in request.form:
        email = request.form['inputEmail']
        fa_auth.update_user(session.get("user_id"),email = email)
        flash("Your email has been updated, please log in again")
        return redirect(url_for("auth.login"))
    if 'inputPassword' in request.form:
        password = request.form['inputPassword']
        fa_auth.update_user(session.get("user_id"),password = password)
        flash("Your password has been updated, please log in again")
        return redirect(url_for("auth.login"))

@profile.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="images/" + filename))

@profile.route("/display")
def display_default():
    return redirect(url_for("static", filename="images/photo_icon.jpeg"))
