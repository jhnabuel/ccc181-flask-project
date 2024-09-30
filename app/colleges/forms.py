from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CollegeForm(FlaskForm):
    code = StringField('College Code', validators=[DataRequired()])
    name = StringField('College Name', validators=[DataRequired()])