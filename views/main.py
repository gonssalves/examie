from flask import render_template, redirect, url_for, session
from flask import Blueprint, request
from flask_login import login_required

#HERE THE VIEWS ARE CREATED
#VIEWS ARE FUNCTIONS RESPONSIBLE FOR HANDLING REQUESTS
#ASSIGNING A URL TO A VIEW GENERATES A ROUTE

#create blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    ''' Verify if there's any user information stored in session, if so, redirect for login page. '''
    
    #by default, Flask-Login uses sessions for authentication
    #session is a dictionary that the application uses to store values that are "remembered" beetween requests

    #session.clear()
    
    #_user_id is added to session if the user is authenticated through login_user() 
    if '_user_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('auth.login'))

@main.route('/question', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def question():
    return render_template('question.html')

@main.route('/exam', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def exam():
    return render_template('exam.html')

@main.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def user():
    return render_template('user.html')


