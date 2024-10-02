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

