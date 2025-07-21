from flask import Flask
from application.database import db
app = None

def app__create():
    app = Flask(__name__)
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.sqlite3"
    db.init_app(app)
    app.app_context().push()
    return app

app = app__create()
from application.controllers import *


if __name__ == '__main__':
    app.run()

