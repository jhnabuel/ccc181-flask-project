from flask import render_template
from . import colleges  # Import the students Blueprint from __init__.py

# Define a route for '/student' under the students blueprint
@colleges.route('/college')
def college_page():
    return render_template('college/college.html')