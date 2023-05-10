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
    return render_template('questions.html')

@main.route('/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def exams():
    return render_template('exams.html')

from login_required import admin_login_required
@main.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_login_required()
def users():
    from models.entities import User
    from forms import SignupForm

    all_users = User.show_all()
    form = SignupForm()

    if form.validate_on_submit():
        from models.auth import auth_signup
        return auth_signup() 
    return render_template('users.html', users=all_users, form=form)

@main.route('/users/<int:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_login_required()
def edit_users(user_id):
    from models.entities import User
    from forms import SignupForm

    user = User.query.filter_by(id=user_id).first()
    form = SignupForm(obj=user)

    if form.validate_on_submit():
        from models.auth import auth_edit
        return auth_edit(user)
    return render_template('edit_users.html', form=form)

@main.route('/users/<int:user_id>/delete', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_login_required()
def delete_users(user_id):
    from models.entities import User

    user = User.query.filter_by(id=user_id).first()
  
    from models.auth import auth_delete
    return auth_delete(user)




