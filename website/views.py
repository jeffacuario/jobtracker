from flask import Blueprint, render_template, request

import website.models.db as db
import website.models.analytics as analysis
from website.models.models import Application
from datetime import date

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
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


@views.route('/analytics', methods=['GET', 'POST'])
def analytics():
    """
    Render Analytics Page
    """
    if request.method == 'POST':
        # To be determined if a search is needed.
        return '', 403

    elif request.method == "GET":
        # Get request

        return render_template("analytics/analytics.html")

    return 'Method not allowed', 405


@views.route('/analytics/generate-charts', methods=['POST'])
def analytics_generate():
    """
    Acts as a URI for use with JS to fetch - allows refresh.
    """
    analysis.generate_charts()
    return '', 204


@views.route('/settings')
def settings():
    """
    Render Settings Page
    """
    return render_template("settings/settings.html")
