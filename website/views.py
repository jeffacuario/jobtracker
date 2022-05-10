from flask import Blueprint, render_template, request, redirect, url_for
from website.auth import login_required

import website.models.db as db
import website.models.analytics as analysis
from website.models.models import Application, Skill
from datetime import date

views = Blueprint('views', __name__)


@views.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    """Render Jobs Page"""
    if request.method == 'POST':
        data = request.form.to_dict()
        data['date'] = date.today().strftime("%B %d, %Y")
        app = Application(data['company'], data['position'], data['type'], data['date'], data['status'])
        db.addJob(app)
        return render_template("jobs/jobs.html", jobs=db.getJobs())
    else:
        return render_template("jobs/jobs.html", jobs=db.getJobs())


@views.route('/jobs/<jobID>/delete', methods=['GET'])
@login_required
def deleteJob(jobID):
    """ Route for deleting Job """
    db.deleteJob(jobID)
    return redirect(url_for('views.jobs'))


@views.route('/skills', methods=['GET', 'POST'])
@login_required
def skills():
    """Render Skills Page"""
    if request.method == 'POST':
        data = request.form.to_dict()
        x = data['position'].split('-')
        skill = Skill(data['skill'], x[0], x[1])
        db.addSkill(skill)
        return render_template("skills/skills.html", skills=db.getSkills(), jobs=db.getJobs())
    else:
        return render_template("skills/skills.html", skills=db.getSkills(), jobs=db.getJobs())


@views.route('/skills/<skillID>/delete', methods=['GET'])
@login_required
def deleteSkill(skillID):
    """ Route for deleting Skill """
    db.deleteSkill(skillID)
    return redirect(url_for('views.skills'))


@views.route('/contacts')
@login_required
def contacts():
    """Render Contacts Page"""
    return render_template("contacts/contacts.html")


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
                "Entries Recorded",
                "Application Statuses",
                "Companies Applied",
                "Position Types",
                "Positions Applied",
                "Your Skills"
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
