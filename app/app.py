from flask import render_template
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from views import app_views
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

app.url_map.strict_slashes = False
app.register_blueprint(app_views)

db_user = getenv('DB_USER')
db_password = getenv('DB_PASSWORD')
db_host = getenv('DB_HOST')
db_name = getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)