from flask import render_template
from . import courses  # Import the students Blueprint from __init__.py

# Define a route for '/student' under the students blueprint
@courses.route('/course')
def course_page():
    return render_template('courses/course.html')