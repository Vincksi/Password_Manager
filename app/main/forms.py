from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class PasswordForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=64)])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    url = StringField('URL', validators=[Optional(), Length(max=256)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Password')

class PasswordGeneratorForm(FlaskForm):
    length = IntegerField('Length', validators=[NumberRange(min=8, max=64)], default=16)
    include_uppercase = BooleanField('Include Uppercase', default=True)
    include_lowercase = BooleanField('Include Lowercase', default=True)
    include_numbers = BooleanField('Include Numbers', default=True)
    include_special = BooleanField('Include Special Characters', default=True)
    generate = SubmitField('Generate Password')