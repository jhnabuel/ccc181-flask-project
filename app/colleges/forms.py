from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Regexp

class CollegeForm(FlaskForm):
    code = StringField('College Code', validators=[DataRequired(), Regexp('^[A-Za-z]+$', message="College Code must contain only letters.")])
    name = StringField('College Name', validators=[DataRequired(), Regexp('^[A-Za-z\s]+$', message="College Name must contain only letters.")])