from flask import Blueprint, render_template, request

import website.models.db as db
from website.models.models import Application
from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import os
from firebase_admin import firestore

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


@views.route('/analytics')
def analytics():
    """
    Render Analytics Page
    """
    return render_template("analytics/analytics.html")


@views.route('/analytics/chart-gen')
def analytics_chart_generator():
    """
    Obscured URI to generate the appropriate charts on demand.
    """
    # Reference to matplotlib docs
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    plt.bar(['Trading', 'Standup', 'Cryptography', 'TEST', 'Javascript'], [10, 5, 5, 8, 1])
    plt.xlabel('Skills')
    plt.ylabel('Frequency')
    plt.title('FAKE DATA Skills Bar chart')
    plt.savefig('website/static/images/chart1.png')
    plt.close()

    plt.bar(['Java', 'Standup', 'Python', 'C++', 'Javascript'], [5, 2, 20, 8, 2])
    plt.xlabel('Skills')
    plt.ylabel('Frequency')
    plt.title('FAKE DATA Overall Skills Bar chart')
    plt.savefig('website/static/images/chart2.png')
    plt.close()

    return '', 204  # No content to be returned to the user.


@views.route('/settings')
def settings():
    """
    Render Settings Page
    """
    return render_template("settings/settings.html")
