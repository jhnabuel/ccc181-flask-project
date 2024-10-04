from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms.validators import DataRequired, ValidationError, Regexp, Length
from app.courses.models import Courses

class StudentForm(FlaskForm):
    # id_year must be exactly 4 digits, and id_unique can accept any integer.
    id_year = StringField('ID Year', validators=[
        DataRequired(), 
        Regexp('^[0-9]{4}$', message="ID Year must be exactly 4 digits.")
    ])
    id_unique = StringField('ID Unique', validators=[
        DataRequired(), 
        Regexp('^[0-9]+$', message="ID Unique must only contain numbers.")
    ])
    
    # Firstname and lastname must contain only letters (upper or lowercase).
    firstname = StringField('First Name', validators=[
        DataRequired(), 
        Regexp('^[A-Za-z]+$', message="First Name must contain only letters.")
    ])
    lastname = StringField('Last Name', validators=[
        DataRequired(), 
        Regexp('^[A-Za-z]+$', message="Last Name must contain only letters.")
    ])
    
    # Course code is a dropdown populated dynamically from the Courses model.
    course_code = SelectField('Course Code', coerce=str, validators=[DataRequired()])
    
    # Year dropdown with fixed choices.
    year = SelectField('Year', validators=[DataRequired()], choices=[
        ('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')
    ])
    
    # Gender dropdown with predefined choices.
    gender = SelectField('Gender', validators=[DataRequired()], choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Non-binary', 'Non-binary'), ('Others', 'Others')
    ])

    def set_course_choices(self):
        # Assuming you have a method 'all' in the Courses class to fetch all courses.
        course_choices = [(course.code, course.code) for course in Courses.get_all_courses()]
        self.course_code.choices = [('', '--Select a Course--')] + course_choices

    def set_year_choices(self):
        self.year.choices = [('', 'Please select a year'), ('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year')]