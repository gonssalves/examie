from flask import render_template, redirect, url_for, session
from flask import Blueprint, request
from flask_login import login_required

#HERE THE VIEWS ARE CREATED
#VIEWS ARE FUNCTIONS RESPONSIBLE FOR HANDLING REQUESTS
#ASSIGNING A URL TO A VIEW GENERATES A ROUTE

#create blueprint
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')
 
@main.route('/questions', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def questions():
    print(session)
    return render_template('questions.html')

@main.route('/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def exams():
    print(session)
    return render_template('exams.html')

from login_required import admin_login_required
@main.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_login_required()
def users():
    print(session)
    from models.entities import User
    all_users = User.show_all()
    return render_template('users.html', users=all_users)


