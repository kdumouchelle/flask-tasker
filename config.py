__author__ = 'Kyle Dumouchelle'
import os

#grab the folder where this script lives
dir = os.path.abspath(os.path.path.dirname(__file__))
DATABASE="taskr.db"
USERNAME = 'kid'
PASSWORD = 'squid'
WTF_CSRF_ENABLED = True
SECRET_KEY = "b'jo\xd6\x05\x8e\xfd\x1b\xf7\xe9\xa1\x1aQ\xd6S\x1a\xd3Z\x0b\xca\xb4'"

#define the full path for the database
DATABASE_PATH = os.path.join(dir, DATABASE)