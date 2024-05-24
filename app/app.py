from flask import Flask, request, g

# from flask_sqlalchemy_app.env import db
from flask_babel import Babel

from app.config.config import config
from app.env import db
from app.admin import admin


def get_locale():
    return request.accept_languages.best_match(['de', 'fr', 'en'])


def create_app():
    app = Flask(__name__)
    app.config.update(config)
    app.config["FLASK_ADMIN_FLUID_LAYOUT"] = True
    db.init_app(app)
    admin.init_app(app)
    babel = Babel(app, locale_selector=get_locale)


    from app.blueprint import routes

    app.register_blueprint(routes)
    return app


