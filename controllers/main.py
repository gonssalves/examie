from flask import render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import InputRequired
from flask import Blueprint
from flask_login import login_required, login_user

#HERE THE VIEWS ARE CREATED
#VIEWS ARE FUNCTIONS RESPONSIBLE FOR HANDLING REQUESTS
#ASSIGNING A URL TO A VIEW GENERATES A ROUTE

#create blueprint
main = Blueprint('main', __name__)

class LoginForm(FlaskForm):
    #Form is sent to template through Jinja2. Some front-end validations
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    choices = [('2', 'Student'), ('3', 'Teacher'), ('1', 'Administrator')]
    select_field = SelectField('Select User Role', choices=choices)
    submit = SubmitField('Submit')

#custom page for client-side error
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#custom page for server-side error
@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@main.route('/')
def index():
    #by default, Flask-Login uses sessions for authentication
    #verify if there's any user information stored in session
    #session is a dictionary that the application uses to store values that are "remembered" beetween requests

    session.clear()
    
    #_user_id is added to session if the user is authenticated through login_user() 
    if '_user_id' in session:
        return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.login'))

#instantiates the form class and invoke function responsible for login validation
#see that I'm not using request.methods explicitly TODO: Check what validate_on_submit returns (proly just a boolean)
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        from models.forms import form_login
        return form_login()
    return render_template('login.html', form=form)

#TODO: Exclude flask-bootstrap from application and create the other routes
@main.route('/home')
@login_required
def home():
    form = SignupForm()
    return render_template('home.html', form=form)
