from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp

class AccountRecoveryForm(FlaskForm):
    #
    email = StringField(validators=[InputRequired()])
    submit = SubmitField('Send Email')

class LoginForm(FlaskForm):
    #Form is sent to template through Jinja2. Some front-end validations
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class PasswordResetForm(FlaskForm):
    #
    password = PasswordField(validators=[InputRequired()])
    password2 = PasswordField('Re-enter Password', 
        validators=[
            InputRequired()
        
        ]
    )
    submit = SubmitField('Change Password')

class SignupForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(), 
            Length(3, message="Username must be at least 3 characters long"), 
            Regexp( 
                "^[A-Za-z][A-Za-z0-9_.]*$", 
                0, 
                "Usernames must have only letters, " "numbers, dots or underscores"
            )
        ]
    )
    email = StringField(
        validators=[
            InputRequired(),
        ]
    )
    
    choices = [('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Administrator')]
    role = SelectField('Select User Role', choices=choices)
    submit = SubmitField('Sign Up')