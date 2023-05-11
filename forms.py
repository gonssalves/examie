from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, RadioField, SubmitField
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
    submit = SubmitField('Submit')


class QuestionForm(FlaskForm):
    level_choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', ('5'))]
    answer_type_choices = [('op', 'Open Question'), ('mc', 'Multiple Choice'), ('sc', 'Single Choice'), ('tf', 'True or False')]
    answer_choices = [('Answer1', 'Answer1'), ('Answer2', 'Answer2'), ('Answer3', 'Answer3'), ('Answer4', 'Answer4')]
    true_or_false_choices = [('True', 'True'), ('False', 'False')]

    subject = StringField(validators=[InputRequired()])
    theme = StringField(validators=[InputRequired()])
    description = StringField(validators=[InputRequired()])
    level = SelectField('Select the Question Level', choices=level_choices)
    tags = StringField(validators=[InputRequired()])
    answer_type = SelectField('Select the Question Type', choices=answer_type_choices)
    answer1 = StringField()
    answer2 = StringField()
    answer3 = StringField()
    answer4 = StringField()
    single_right_answer = RadioField('Select the Right Answer', choices=answer_choices)
    true_or_false_answer = RadioField('Is the Answer', choices=true_or_false_choices)
    multiple_right_answer1 = BooleanField('Answer1')
    multiple_right_answer2 = BooleanField('Answer2')
    multiple_right_answer3 = BooleanField('Answer3')
    multiple_right_answer4 = BooleanField('Answer4')
    submit = SubmitField('Submit')

class ExamForm(FlaskForm):
    opening_time = StringField('Opening Time', validators=[InputRequired()])
    closing_time = StringField('Closing Time', validators=[InputRequired()])
    execution_time = StringField('Execution Time', validators=[InputRequired()])
    submit = SubmitField('Submit')