from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv

db_user = getenv('DB_USER')
db_password = getenv('DB_PASSWORD')
db_host = getenv('DB_HOST')
db_name = getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name)
print("Database URI:", SQLALCHEMY_DATABASE_URI)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)