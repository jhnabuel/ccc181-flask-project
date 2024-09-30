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
            # Check if college already exists
            existing_college = Colleges.get_by_code(form.code.data)
            if existing_college:
                flash('Error: College with this code already exists.', 'danger')
                return render_template('college/add_college.html', form=form)

            college = Colleges(code=form.code.data, name=form.name.data)
            try:
                college.add_college()
                flash('College added successfully', 'success')
                return redirect(url_for('colleges.college_page'))
            except IntegrityError as e:
                print(f"Error: {e}")  # Print error details for debugging
                flash('Error: Failed to add college.', 'danger')

    return render_template('college/add_college.html', form=form)


@colleges.route("/delete_college/<string:code>", methods=['POST'])
def delete_college(code):
    print(f"Attempting to delete college with code: {code}")
    college = Colleges.get_by_code(code)
    if college is None:
        print("College not found.")
        flash('Error: College not found.', 'danger')
        return redirect(url_for('colleges.college_page'))

    try:
        college.delete_college()
        flash('College deleted successfully', 'success')
        print("College deleted successfully.")
    except Exception as e:
        print(f"Error during deletion: {e}")
        flash('Error: Failed to delete college.', 'danger')

    return redirect(url_for('colleges.college_page'))
