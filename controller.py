from flask import render_template, redirect, url_for, session
from flask import Blueprint, request
from flask_login import login_required

#HERE THE VIEWS ARE CREATED
#VIEWS ARE FUNCTIONS RESPONSIBLE FOR HANDLING REQUESTS
#ASSIGNING A URL TO A VIEW GENERATES A ROUTE

#create blueprint
controller = Blueprint('controller', __name__)

#custom page for client-side error
@controller.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#custom page for server-side error
@controller.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@controller.route('/')
def index():
    ''' Verify if there's any user information stored in session, if so, redirect for login page. '''
    
    #by default, Flask-Login uses sessions for authentication
    #session is a dictionary that the application uses to store values that are "remembered" beetween requests

    #session.clear()
    
    #_user_id is added to session if the user is authenticated through login_user() 
    if '_user_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('controller.login'))

@controller.route('/login', methods=['GET', 'POST'])
def login():
    ''' Login validation. '''
    from forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit(): #see that I'm not using request.methods explicitly  
        from models.auth import auth_login
        return auth_login()
    form.process(request.args)
    return render_template('login.html', form=form)
        
@controller.route('/signup', methods=['GET', 'POST'])
@login_required
def signup():
    ''' Check if the form is submitted. '''
    from forms import SignupForm
    form = SignupForm()
    if form.validate_on_submit():
        from models.auth import auth_signup
        return auth_signup() 
    form.process(request.args)#insert the request parameter in the form
    return render_template('signup.html', form=form)
