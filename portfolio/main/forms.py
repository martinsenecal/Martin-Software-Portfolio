from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class ResumeForm(FlaskForm):
    email = StringField('Your Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
