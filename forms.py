from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp

class LoginForm(FlaskForm):
    #Form is sent to template through Jinja2. Some front-end validations
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Submit')

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
    password = PasswordField(
        validators=[
            InputRequired(), 
            Length(8, 16, message="Password must be between 8 and 16 characters long"
            )
        ]
    )
    re_password = PasswordField('Re-enter Password', 
        validators=[
            InputRequired(),
            Length(8, 16, message='Passwords must be the same')
]
    )
    
    choices = [('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Administrator')]
    role = SelectField('Select User Role', choices=choices)
    submit = SubmitField()