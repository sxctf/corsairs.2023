import os

file_log = os.path.abspath(os.getcwd()) + "/logs/TS_Events.log"
file_db = os.path.abspath(os.getcwd())+"/data/taskstate.db"
FLASK_APP = 'TS_app'
FLASK_ENV = 'CTFdev'
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+file_db
SQLALCHEMY_TRACK_MODIFICATIONS = False
