from flask import Blueprint


routes = Blueprint("main", __name__)

from app.env import db


@routes.route("/test")
def test():
    pass
