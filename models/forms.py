from models.entities import User
from flask import request, redirect, url_for, flash
from flask_login import login_user

def form_login():
    ''' Check if the user exists in the database and if the information submitted is correct.'''
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        if user.verify_password(password):
            login_user(user)#once user is authenticated, he is logged with this function
            return redirect(url_for('main.home'))
    flash('Invalid username or password.')#TODO: I want flash to keep the information typed in the form  
    return redirect(url_for('main.login'))

def form_signup():
    ...