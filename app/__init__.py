from flask import Flask
from app.dbsession import create_session as create_db_session

app = Flask(__name__)
db = create_db_session()

from app.views import *