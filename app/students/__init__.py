from flask import Blueprint

# Create the Blueprint for students
students = Blueprint('students', __name__)

# Import the routes from the routes.py file
from . import routes