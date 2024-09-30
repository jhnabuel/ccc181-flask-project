from flask import render_template, request, redirect, flash, url_for
from . import colleges  # Import the college Blueprint from __init__.py
from app.colleges.models import Colleges
from app.colleges.forms import CollegeForm
from app import mysql
from pymysql import IntegrityError


# Define a route for '/college' under the college blueprint
@colleges.route('/college', methods=['GET'])
def college_page():
    search_term = request.args.get('search_term', '')  # Get the search term
    search_by = request.args.get('search_by', 'college-name')  # Default to 'college-name'

    colleges_list = Colleges.get_all_colleges(search_by, search_term)
    return render_template('college/college.html', colleges=colleges_list, selected_info=search_by, search_term=search_term)

@colleges.route("/add_college", methods=['POST', 'GET'])
def add_college():
    form = CollegeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            college = Colleges(code=form.code.data, name=form.name.data)
            try:
                college.add_college()
                flash('College added successfully', 'success')
                return redirect(url_for('colleges.college_page'))
            except IntegrityError as e:
                if "Duplicate entry" in str(e.args):
                    flash('Error: College with this code already exists.', 'danger')
                else:
                    flash('Error: Failed to add college.', 'danger')
        else:
            flash('Error: All fields are required.', 'danger')
            print(form.errors)
    return render_template('college/add_college.html', form=form)