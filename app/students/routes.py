from flask import render_template, request, redirect, flash, url_for
from app.students.models import Students
from . import students  # Import the students Blueprint from __init__.py
from app import mysql
from pymysql import IntegrityError

# Define a route for '/student' under the students blueprint
@students.route('/student', methods=['GET'])
def student_page():
    search_term = request.args.get('search_term', '')  # Get the search term
    search_by = request.args.get('search_by', 'student-id')  # Default to 'course-name'

    students_list = Students.get_all_students(search_by, search_term)
    return render_template('student/student.html', students=students_list, selected_info=search_by, search_term=search_term)