from models.entities import User, Role
from flask import request, redirect, url_for, flash
from flask_login import login_user
from app import bcrypt

def form_login():
    ''' Check if the user exists in the database and if the information submitted is correct.'''
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        if user.verify_password(password):
            login_user(user)#once user is authenticated, he is logged with this function
            return redirect(url_for('controller.signup'))
    flash('Invalid username or password.')#TODO: I want flash to keep the information typed in the form  
    return redirect(url_for('controller.login'))

def form_signup():
    ''' Register an user'''
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    email = User.query.filter_by(email=email).first()

    if email:
        flash('Email already exists')
        return redirect(url_for('controller.signup'))
    
    username = User.query.filter_by(username=username).first()

    if username:
        flash('User already exists')
        return redirect(url_for('controller.signup'))
    
    password = bcrypt.generate_password_hash(password).decode('utf-8')

    role = Role.query.get(int(role))
    
    new_user = User(username=username, email=email, password=password, role=role)


    return 'new_user.role'
