from flask import Blueprint, render_template, request, redirect, url_for, g
from website.auth import login_required

import website.models.db as db
import website.models.analytics as analysis
from website.models.models import Application, Contact, Skill
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    """Render Jobs Page"""
    userID = g.user['users'][0]['localId']
    typeList = ['Full-Time', 'Part-Time', 'Internship']

    if request.method == 'POST':
        data = request.form.to_dict()
        data['date'] = str(datetime.now())
        data['userID'] = userID
        app = Application(data)
        jobs = db.getJobs(userID)

        if len(jobs) == 0:
            db.addJob(app)
            return render_template("jobs/jobs.html", jobs=db.getJobs(userID), alert=0, typeList=typeList)

        # handle duplicate entry
        for item in jobs:
            if app.company == item['company'] and app.position == item['position'] and app.type == item['type']:
                return render_template("jobs/jobs.html", jobs=jobs, alert=1, typeList=typeList)

        db.addJob(app)
        return render_template("jobs/jobs.html", jobs=db.getJobs(userID), alert=0, typeList=typeList)
    else:
        return render_template("jobs/jobs.html", jobs=db.getJobs(userID), typeList=typeList)


@views.route('/jobs/<jobID>/delete', methods=['GET'])
@login_required
def deleteJob(jobID):
    """ Route for deleting Job """
    db.deleteJob(jobID, g.user['users'][0]['localId'])
    return redirect(url_for('views.jobs'))


@views.route('/jobs/<jobID>/update', methods=['POST'])
@login_required
def updateJob(jobID):
    """ Route for updating Job """
    data = request.form.to_dict()
    db.updateJob(jobID, data, g.user['users'][0]['localId'])
    return redirect(url_for('views.jobs'))


@views.route('/skills', methods=['GET', 'POST'])
@login_required
def skills():
    """Render Skills Page"""
    userID = g.user['users'][0]['localId']
    if request.method == 'POST':
        data = request.form.to_dict()
        data['userID'] = userID

        add = Skill(data)
        skills = db.getSkills(userID)
        jobs = db.getJobs(userID)

        if len(skills) == 0:
            db.addSkill(add)
            return render_template("skills/skills.html", skills=db.getSkills(userID), jobs=jobs, alert=0)

        # handle duplicate entry
        for item in skills:
            if add.skill == item['skill'] and add.posID == item['posID']:
                return render_template("skills/skills.html", skills=skills, jobs=jobs, alert=1)

        db.addSkill(add)
        return render_template("skills/skills.html", skills=db.getSkills(userID), jobs=jobs, alert=0)
    else:
        return render_template("skills/skills.html", skills=db.getSkills(userID), jobs=db.getJobs(userID))


@views.route('/skills/<skillID>/delete', methods=['GET'])
@login_required
def deleteSkill(skillID):
    """ Route for deleting Skill """
    db.deleteSkill(skillID)
    return redirect(url_for('views.skills'))


@views.route('/skills/<skillID>/update', methods=['POST'])
@login_required
def updateSkill(skillID):
    """ Route for updating Skill """
    data = request.form.to_dict()
    db.updateSkill(skillID, Skill(data))
    return redirect(url_for('views.skills'))


@views.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():
    """Render Contacts Page"""
    userID = g.user['users'][0]['localId']
    if request.method == 'POST':
        data = request.form.to_dict()
        data['userID'] = userID
        # default image
        data['img'] = 'https://bit.ly/3yKJCvq'

        if request.files['img']:
            img = request.files['img']
            data['img'] = db.addContactImage(img, userID)

        add = Contact(data)
        contacts = db.getContacts(userID)
        jobs = db.getJobs(userID)

        if len(contacts) == 0:
            db.addContact(add)
            return render_template("contacts/contacts.html", contacts=db.getContacts(userID), jobs=jobs, alert=0)

        # handle duplicate entry
        checkList = ['fName', 'lName', 'title', 'email']
        for item in contacts:
            count = 0
            for i in checkList:
                if add.__getattribute__(i) == item[i]:
                    count += 1
            if count == len(checkList):
                return render_template("contacts/contacts.html", contacts=contacts, jobs=jobs, alert=1)

        db.addContact(add)
        return render_template("contacts/contacts.html", contacts=db.getContacts(userID), jobs=jobs, alert=0)            
    else:
        return render_template("contacts/contacts.html", contacts=db.getContacts(userID), jobs=db.getJobs(userID))


@views.route('/contacts/<contactID>/delete', methods=['GET'])
@login_required
def deleteContact(contactID):
    """ Route for deleting Contact """
    db.deleteContact(contactID)
    return redirect(url_for('views.contacts'))


@views.route('/contacts/<contactID>/update', methods=['POST'])
@login_required
def updateContact(contactID):
    """ Route for updating Contact """
    userID = g.user['users'][0]['localId']

    data = request.form.to_dict()
    data['userID'] = userID
    if request.files['img']:
        img = request.files['img']
        data['img'] = db.addContactImage(img, userID)
    else:
        data['img'] = db.getContactImgURL(contactID)['img']
        
    db.updateContact(contactID, Contact(data))
    return redirect(url_for('views.contacts'))


@views.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics():
    """ Render Analytics Page """
    if request.method == 'POST':
        # To be determined if a search is needed.
        return '', 403

    elif request.method == "GET":
        # Get request

        data = {
            "charts": [
                "Your Insights",
                "Your Job Titles Applied",
                "Companies Applied",
                "Position Types",
                "Positions Applied",
                "Your Skills",
                "Your Entries over time"
            ]
        }

        return render_template("analytics/analytics.html", data=data)

    return 'Method not allowed', 405


@views.route('/analytics/generate-charts', methods=['POST'])
@login_required
def analytics_generate():
    """ Acts as a URI for use with JS to fetch - allows refresh."""
    analysis.generate_charts(request.json)
    return '', 204


@views.route('/')
def home():
    """Render Landing Page"""
    return render_template("landing.html")
