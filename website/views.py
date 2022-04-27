from flask import Blueprint, render_template, request

import website.models.db as db
from website.models.models import Application
from datetime import date


views = Blueprint('views', __name__)


@views.route('/jobs', methods=['GET', 'POST'])
def jobs():
    """
    Render Jobs Page
    """
    if request.method == 'POST':
        data = request.form.to_dict()
        data['date'] = date.today().strftime("%B %d, %Y")
        app = Application(data['company'], data['position'], data['type'], data['date'], data['status'])
        db.addJob(app)
        return render_template("jobs/jobs.html", jobs=db.getJobs())
    else:
        return render_template("jobs/jobs.html", jobs=db.getJobs())


@views.route('/skills')
def skills():
    """
    Render Skills Page
    """
    return render_template("skills/skills.html")


@views.route('/contacts')
def contacts():
    """
    Render Contacts Page
    """
    return render_template("contacts/contacts.html")


@views.route('/analytics')
def analytics():
    """
    Render Analytics Page
    """
    return render_template("analytics/analytics.html")


@views.route('/settings')
def settings():
    """
    Render Settings Page
    """
    return render_template("settings/settings.html")


@views.route('/')
def home():
    """
    Render Landing Page
    """
    return render_template("landing.html")
    