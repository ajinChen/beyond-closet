from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from connection import test_connection
from utils import get_yaml_file
import os
import boto3

conn_url = os.environ.get('SQLALCHEMY_DATABASE_URI')

class Config(object):
    db_name = 'postgres'
    SECRET_KEY = os.urandom(24)
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

# initialize flask app with config
app = Flask(__name__)
app.config.from_object(Config)

# login_manager for flask
login_manager = LoginManager()
login_manager.init_app(app)

# Postgres database instance
db = SQLAlchemy(app)

# test connection to postgres database
test_connection(conn_url)

# get yaml file
team_members_yaml = get_yaml_file()

# initialize S3 bucket
bucket_name = os.getenv('AWS_BUCKET_NAME')
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
