from flask import Blueprint, render_template

main = Blueprint('main', __name__)

# Define the route for the home page
@main.route('/')
def index():
    return render_template('index.html')  # Specify the path to index.html
