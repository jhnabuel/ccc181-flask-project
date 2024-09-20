from flask import render_template
from . import students  # Import the students Blueprint from __init__.py

# Define a route for '/student' under the students blueprint
@students.route('/student')
def student_page():
    return render_template('student/student.html')