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
