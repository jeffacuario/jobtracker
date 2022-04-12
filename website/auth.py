from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """
    Render Login Page
    """
    return render_template("auth/login.html")

@auth.route('/register')
def register():
    """
    Render Register Page
    """
    return render_template("auth/register.html")