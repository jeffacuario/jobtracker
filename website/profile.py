from flask import Blueprint, render_template, request, redirect, url_for, \
    session, send_file, g, flash
import requests
from firebase_admin import auth as fa_auth
import website.models.db as db
from website.pyre import fb_storage


profile = Blueprint("profile", __name__)

# reference: https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "webp"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in \
        ALLOWED_EXTENSIONS


@profile.route("/settings")
def settings_page():
    userID = g.user['users'][0]['localId']
    jobs = db.getJobs(userID)
    roles = []
    companies = []
    types = []
    for i in range(len(jobs)):
        if jobs[i]['position'] not in roles:
            roles.append(jobs[i]['position'])
        if jobs[i]['company'] not in companies:
            companies.append(jobs[i]['company'])
        if jobs[i]['type'] not in types:
            types.append(jobs[i]['type'])
    skill_res = db.getSkills(userID)
    skills = []
    for i in range(len(skill_res)):
        if skill_res[i]['skill'] not in skills:
            skills.append(skill_res[i]['skill'])
    return render_template("settings/settings.html",
                           roles=", ". join(roles), companies=", ".
                           join(companies), types=", ". join(types),
                           skills=", ". join(skills))


@profile.route("/settings", methods=["POST"])
def update_file():
    if "file" in request.files:
        file = request.files["file"]
        if file and allowed_file(file.filename):
            user_uid = session.get("user_id")
            path_on_cloud = "profile_images/" + user_uid + "/" + file.filename
            upload = fb_storage.child(path_on_cloud).put(
                file, session.get("token_id")
            )
            image_url = fb_storage.child(path_on_cloud).get_url(
                upload["downloadTokens"]
            )
            fa_auth.update_user(session.get("user_id"), photo_url=image_url)
        # return redirect(url_for("profile.settings_page"))
        return render_template("settings/settings.html", alert=2)
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
    default_url = "https://firebasestorage.googleapis.com/v0/b/jobtrack-\
    39d73.appspot.com/o/photo_icon.jpeg?alt=media&token=e1c9c533-0aa1-\
    44bb-b465-762fd9d1b928"
    r = requests.get(default_url, stream=True)
    res = r.raw
    return send_file(res, mimetype='image/jpeg')
