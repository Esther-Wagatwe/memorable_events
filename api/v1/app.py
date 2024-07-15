#!/usr/bin/python3
"""module to start an api"""


from flask import Flask
from api.v1.routes import app_views
from flask_sqlalchemy import SQLAlchemy
from api.v1.routes import db


app = Flask(__name__)


app.url_map.strict_slashes = False
app.register_blueprint(app_views)

# Configure SQLAlchemy for MySQL on web-01 server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://memorable_events:1Wagatwe@52.91.124.142/memorable_events_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
