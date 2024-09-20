from flask import Blueprint

# Create the Blueprint for students
colleges = Blueprint('colleges', __name__)

# Import the routes from the routes.py file
from . import routes