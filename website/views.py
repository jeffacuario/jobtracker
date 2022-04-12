from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def jobs():
    """
    Render Jobs Page
    """
    return render_template("jobs/jobs.html")


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
