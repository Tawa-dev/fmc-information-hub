from re import I
from flask import Flask

app = Flask(__name__)

from app import views
from app import leave_views
from app import travel_view
from app import asset_view
from app import main_views
from app.database import Database


@app.before_first_request
def initialize_database():
    Database.initialize()
