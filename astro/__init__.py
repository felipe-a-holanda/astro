from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.appconfig import AppConfig


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)
    
    return app

app = create_app('default.cfg')
db = MongoEngine(app)

from astro import views
    
if __name__ == "__main__":
    app.run()

