from flask import render_template
from . import colleges  # Import the students Blueprint from __init__.py
from .models import Colleges
# Define a route for '/student' under the students blueprint
@colleges.route('/college', methods=['GET'])
def college_page():
    colleges_list = Colleges.get_all_colleges()
    return render_template('college/college.html', colleges=colleges_list)