from flask import render_template
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

db_user = getenv('DB_USER')
db_password = getenv('DB_PASSWORD')
db_host = getenv('DB_HOST')
db_name = getenv('DB_NAME')

# Configure SQLAlchemy for MySQL on web-01 server
SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name)
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)

# db_user = getenv('DB_USER')
# db_password = getenv('DB_PASSWORD')
# db_host = getenv('DB_HOST')
# db_name = getenv('DB_NAME')

# SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name)
# print("Database URI:", SQLALCHEMY_DATABASE_URI)
#engine = create_engine(SQLALCHEMY_DATABASE_URI)
# try:
#     engine = create_engine(SQLALCHEMY_DATABASE_URI)
#     # Try to connect
#     with engine.connect() as connection:
#         print("Database connection successful!")
# except Exception as e:
#     print("Error connecting to database:", e)

# Session = sessionmaker(bind=engine)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)