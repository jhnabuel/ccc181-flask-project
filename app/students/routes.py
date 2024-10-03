from flask import render_template, request, redirect, flash, url_for
from app.students.models import Students
from app.students.forms import StudentForm
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

@students.route("/add_student", methods=['POST', 'GET'])
def add_student():
    form = StudentForm()

    # Load the courses for the dropdown
    form.set_course_choices()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Combine id_year and id_unique to form student_id
            student_id = f"{form.id_year.data}-{form.id_unique.data}"

            # Check if student with this ID already exists
            existing_student = Students.get_by_id(student_id)
            if existing_student:
                flash('Error: A student with this ID already exists.', 'danger')
                return render_template('student/add_student.html', form=form)

            # Create a new student object
            new_student = Students(
                id_number=student_id,
                first_name=form.firstname.data,
                last_name=form.lastname.data,   
                year_level=form.year.data,
                gender=form.gender.data,
                student_course=form.course_code.data
            )

            try:
                # Add the student to the database
                new_student.add_student()  # Assuming you have a method for adding students
                flash('Student added successfully', 'success')
                return redirect(url_for('students.student_page'))
            except IntegrityError as e:
                print(f"Error: {e}")  # Print error details for debugging
                flash('Error: Failed to add student.', 'danger')

    return render_template('student/add_student.html', form=form)

@students.route("/delete_student/<string:id>", methods=['POST'])
def delete_student(id):
    print(f"Attempting to delete student with ID number: {id}")
    student = Students.get_by_id(id)
    if student is None:
        print("Student not found.")
        flash('Error: Student not found.', 'danger')
        return redirect(url_for('students.student_page'))

    try:
        student.delete_student()
        flash('Student info deleted successfully', 'success')
        print("Student info deleted successfully.")
    except Exception as e:
        print(f"Error during deletion: {e}")
        flash('Error: Failed to delete student info.', 'danger')

    return redirect(url_for('students.student_page'))