from flask import render_template, request, redirect, flash, url_for
from app.students.models import Students
from app.students.forms import StudentForm
from . import students  # Import the students Blueprint from __init__.py
from app import mysql
from pymysql import IntegrityError
import cloudinary, cloudinary.uploader
from cloudinary.uploader import upload

# Define a route for '/student' under the students blueprint
@students.route('/student', methods=['GET'])
def student_page():
    search_term = request.args.get('search_term', '')  # Get the search term
    search_by = request.args.get('search_by', 'student-id')  # Default to 'course-name'

    students_list = Students.get_all_students(search_by, search_term)
    return render_template('student/student.html', students=students_list, selected_info=search_by, search_term=search_term)

def is_image_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'svg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def is_file_size_valid(file_field):
    try:
        file_size = len(file_field.read())
        file_field.seek(0)  # Reset file cursor position
        max_size = 1024 * 1024  # 1 MB

        if file_size > max_size:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error checking file size: {e}")
        return False

@students.route("/add_student", methods=['POST', 'GET'])
def add_student():
    form = StudentForm()
    

    # Load the courses for the dropdown
    form.set_course_choices()

    if request.method == 'POST':
        if form.image_url.data and not is_image_file(form.image_url.data.filename):
            flash('Error: Only image files (jpg, jpeg, png, svg) are allowed for the photo.', 'danger')
            return render_template('student/add_student.html', form=form)
        # Check file-related conditions before calling validate_on_submit
        if not is_file_size_valid(form.image_url.data):
            flash('Error: File size must be no more than 1 MB.', 'danger')      
            return render_template('student/add_student.html', form=form)

        if form.validate_on_submit():
            
            image_url = None
            if form.image_url.data:
                    try:
                        # Use cloudinary.uploader.upload directly
                        response = cloudinary.uploader.upload(form.image_url.data, folder="student_photo")
                        image_url = response['secure_url']
                    except Exception as e:
                        flash(f'Error: Cloudinary upload failed. {e}', 'danger')
                        return render_template('student/add_student.html', form=form)
            else:
                image_url = "https://res.cloudinary.com/dzmgvynf3/image/upload/v1234567890/student_photo/placeholder.jpg"
                    
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
                student_course=form.course_code.data,
                image_url=image_url
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


@students.route("/edit_student/<string:id>", methods=['GET', 'POST'])
def edit_student(id):
    student = Students.get_by_id(id)  # Fetch the student using their ID
    form = StudentForm()  # Initialize the form

    # Split the ID number into year and unique parts
    if request.method == "GET":
        if student and student.id_number:  # Ensure the student and id_number are valid
            id_year, id_unique = student.id_number.split('-')
            form.id_year.data = id_year
            form.id_unique.data = id_unique
            form.firstname.data = student.first_name
            form.lastname.data = student.last_name
            form.year.data = student.year_level
            form.gender.data = student.gender
            form.course_code.data = student.student_course

    # Set the course choices for the dropdown
    form.set_course_choices()

    if request.method == "POST":
        if form.image_url.data:
            if not is_image_file(form.image_url.data.filename):
                flash('Error: Only image files (jpg, jpeg, png, svg) are allowed for the photo.', 'danger')
                return render_template('student/edit_student.html', form=form, student=student, id=id, image_url=student.image_url)
            
            if not is_file_size_valid(form.image_url.data):
                flash('Error: File size must be no more than 1 MB.', 'danger')
                return render_template('student/edit_student.html', form=form, student=student, id=id, image_url=student.image_url)

        if form.validate_on_submit():
            # Initialize image_url to retain the current image by default
            image_url = student.image_url
            placeholder_url = 'https://res.cloudinary.com/dzmgvynf3/image/upload/v1234567890/student_photo/placeholder.jpg'
            # Determine whether to set to placeholder or a new URL
            image_url = student.image_url

            # Check if a new image is uploaded
            if form.image_url.data and image_url != placeholder_url:
                # Flash an error if the user hasn't clicked the remove button
                if request.form.get("remove_image") != "true":
                    flash("Please remove the current photo before uploading a new one.", "danger")
                    return render_template('student/edit_student.html', form=form, student=student, image_url=image_url)

            if form.image_url.data != image_url:
                if request.form.get("remove_image") == "true":  # Remove existing image
                    if student.image_url != placeholder_url:
                        parts = student.image_url.split('/')
                        if 'student_photo' in parts:
                            filename = parts[-1]
                            public_id = filename.split('.')[0]
                            full_public_id = f"student_photo/{public_id}"
                            try:
                                cloudinary.uploader.destroy(full_public_id)
                            except Exception as e:
                                flash(f'Error occurred while trying to delete the image: {e}', 'danger')
                    image_url = placeholder_url
                
            
            # Check if a new image is uploaded after removing
            if form.image_url.data and request.form.get("remove_image") == "true":
                response = cloudinary.uploader.upload(form.image_url.data, folder="student_photo")
                image_url = response['secure_url']
            
            # Upload if photo of student is placeholder photo
            if image_url == placeholder_url:
                if form.image_url.data:
                    response = cloudinary.uploader.upload(form.image_url.data, folder="student_photo")
                    image_url = response['secure_url']

            
            print("Form Data:", form.data)  # Check submitted data
            try:
                # Update the student object with the new data
                student.id_number = f"{form.id_year.data}-{form.id_unique.data}"  # Concatenate back
                student.first_name = form.firstname.data
                student.last_name = form.lastname.data
                student.year_level = form.year.data
                student.gender = form.gender.data
                student.student_course = form.course_code.data
                student.image_url = image_url

                # Save the updated student object
                student.edit_student()
                flash('Student updated successfully', 'success')
                return redirect(url_for('students.student_page'))

            except IntegrityError as e:
                if "Duplicate entry" in str(e.args):
                    flash('Error: Student with this ID already exists.', 'danger')
                else:
                    flash('Error: Failed to update student.', 'danger')
                # Rollback any changes if an integrity error occurs
                mysql.connection.rollback()
        else:
            flash('Error: Please correct the form errors and try again.', 'danger')
            print(form.errors)

    return render_template('student/edit_student.html', form=form, student=student, id=id, image_url=student.image_url)



