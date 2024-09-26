from flask import render_template, request
from . import colleges  # Import the students Blueprint from __init__.py
from .models import Colleges
# Define a route for '/student' under the students blueprint
@colleges.route('/college', methods=['GET'])
def college_page():
    search_term = request.args.get('search_term', '')  # Get the search term
    search_by = request.args.get('search_by', 'college-name')  # Default to 'college-name'

    colleges_list = Colleges.get_all_colleges(search_by, search_term)
    return render_template('college/college.html', colleges=colleges_list, selected_info=search_by)