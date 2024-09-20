from flask import Blueprint

# Create the blueprint for the main routes
main = Blueprint('main', __name__)

# Import routes so they are registered
from . import routes
