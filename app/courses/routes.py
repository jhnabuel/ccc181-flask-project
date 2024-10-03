from flask import render_template, request, redirect, flash, url_for
from app.courses.models import Courses
from app.courses.forms import CourseForm
from . import courses  # Import the students Blueprint from __init__.py
from app import mysql
from pymysql import IntegrityError

# Define a route for '/student' under the students blueprint
@courses.route('/course', methods=['GET'])
def course_page():
    search_term = request.args.get('search_term', '')  # Get the search term
    search_by = request.args.get('search_by', 'course-name')  # Default to 'course-name'

    courses_list = Courses.get_all_courses(search_by, search_term)
    return render_template('courses/course.html', courses=courses_list, selected_info=search_by, search_term=search_term)

@courses.route("/add_course", methods=['POST', 'GET'])
def add_course():
    form = CourseForm()

    # Load the colleges for the dropdown
    form.set_college_choices()

    if request.method == 'POST':
        if form.validate_on_submit():
            existing_course = Courses.get_by_code(form.code.data)
            
            if existing_course:
                flash('Error: College with this code already exists.', 'danger')
                return render_template('courses/add_course.html', form=form)
            
            course = Courses(course_code=form.code.data, course_name=form.name.data, course_college=form.college_code.data)
            try:
               course.add_course()
               flash('Course added successfully', 'success')
               return redirect(url_for('courses.course_page'))
            except IntegrityError as e:
                print(f"Error: {e}")  # Print error details for debugging
                flash('Error: Failed to add course.', 'danger')

    return render_template('courses/add_course.html', form=form)

@courses.route("/delete_course/<string:code>", methods=['POST'])
def delete_course(code):
    print(f"Attempting to delete college with code: {code}")
    course = Courses.get_by_code(code)
    if course is None:
        print("College not found.")
        flash('Error: College not found.', 'danger')
        return redirect(url_for('courses.course_page'))

    try:
        course.delete_course()
        flash('Course deleted successfully', 'success')
        print("Course deleted successfully.")
    except Exception as e:
        print(f"Error during deletion: {e}")
        flash('Error: Failed to delete course.', 'danger')

    return redirect(url_for('courses.course_page'))

@courses.route("/edit_course/<string:code>", methods=['GET','POST'])
def edit_course(code):
    course = Courses.get_by_code(code)
    form = CourseForm(obj=course)
      # Set the college choices for the SelectField
    form.set_college_choices()  # Populate the college choices dynamically
    if request.method == 'POST':
        if form.validate_on_submit():
            new_code = form.code.data
            new_name = form.name.data
            new_college = form.college_code.data
            # Check if the code field is empty or None
            if not new_code:
                flash('Error: Course code cannot be empty.', 'danger')
                return render_template('courses/edit_course.html', form=form, code=code)

            # Check if the code has been changed and if the new code already exists
            if new_code != code:
                existing_course = Courses.get_by_code(new_code)
                if existing_course:
                    flash(f'Error: Course with code "{new_code}" already exists.', 'danger')
                    return render_template('courses/edit_course.html', form=form, code=code)

            # Proceed with updating the college details
            course.name = new_name
            course.new_code = new_code  # Ensure that code is not empty or null
            course.college_code = new_college
            try:
                course.edit_course()  # Pass the original code for comparison
                flash('Course updated successfully', 'success')
                return redirect(url_for('courses.course_page'))

            except IntegrityError as e:
                # Handle database integrity errors
                if "Duplicate entry" in str(e.orig):
                    flash(f'Error: Course with code "{new_code}" already exists.', 'danger')
                elif "cannot be null" in str(e.orig):
                    flash('Error: Course code cannot be null.', 'danger')
                else:
                    flash('Error: Failed to update course.', 'danger')
                print(f"Error: {e}")  # Log the error details for debugging
        else:
            flash('Error: All fields are required.', 'danger')
            print(form.errors)


    return render_template('courses/edit_course.html', form=form, code=code)