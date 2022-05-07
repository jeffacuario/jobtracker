from flask import Flask
from website.models.db import db_init

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'kjaskfjkdsj'

    from .views import views
    from .auth import auth
    from .profile import profile

    app.register_blueprint(views, urlprefix='/')
    app.register_blueprint(auth, urlprefix='/')
    app.register_blueprint(profile, urlprefix='/')

    # Initiate the database connection
    db_init()

    return app
