from models.entities import User, Role
from flask import request, redirect, url_for, flash, session
from flask_login import login_user
from app import db, bcrypt, mail
from email_validator import validate_email, EmailNotValidError
from email.message import EmailMessage
import smtplib
import ssl


def auth_login():
    ''' Check if the user exists in the database and if the information submitted is correct.'''
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = (True if request.form.get('remember_me') else False)
    
    #check if user is on the database
    user = User.query.filter_by(username=username).first()#returns none if there's no such user

    #pop password from the request body
    req = request.form.copy()
    req.pop('password')
    req.pop('csrf_token')
    req.pop('submit')

    if user:
        if user.verify_password(password) or password == user.password:
            login_user(user, remember=remember_me)#once user is authenticated, he is logged with this function | remember-me can keep the user logged after the browser is closed
            return redirect(request.args.get('next') or url_for('main.index'))
    flash('Invalid username or password.')
    return redirect(url_for('auth.login', **req))#**req is used to sent the request to the form, so the user doesn't need to type everything again
    #TODO: search about this url_for parameters

def auth_recovery():#TODO: search how to send email, gmail blocked some shit about "less safe apps" 
    email = request.form.get('email')

    req = request.form.copy()
    req.pop('csrf_token')
    req.pop('submit')

    try:
        emailinfo = validate_email(email, check_deliverability=True)#check_deliverability DNS queries are made to check that the domain name in the email address (the part after the @-sign) can receive mail
        email = emailinfo.normalized#
    except EmailNotValidError as e:
        flash(str(e))
        return redirect(url_for('auth.account_recovery', **req))
    
    user = User.query.filter_by(email=email).first()

    if user:
        password = user.password
        #Define email sender and receiver
        email_sender = 'contacttrepverter@gmail.com'
        email_password = 'ipxtsyzonfvriiem'
        email_receiver = email

        #Set the subject and body of the email
        subject = 'Recovery Account!'
        body = f'Use this password to log in: {password}'

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        
        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    flash('If this email is registered, you received a message. Check your spam box.')
    return redirect(url_for('auth.account_recovery'))

def auth_signup():
    ''' Validate the informations sent and register an user. '''
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    re_password = request.form.get('re_password')
    role = request.form.get('role')

    req = request.form.copy()
    req.pop('password')
    req.pop('csrf_token')
    req.pop('submit')

    #use email_validator package
    try:
        emailinfo = validate_email(email, check_deliverability=True)#check_deliverability DNS queries are made to check that the domain name in the email address (the part after the @-sign) can receive mail
        email = emailinfo.normalized#
    except EmailNotValidError as e:
        flash(str(e))
        return redirect(url_for('auth.signup', **req))

    if password != re_password:
        flash('Passwords must be the same')
        return redirect(url_for('auth.signup', **req))
    
    verify_email = User.query.filter_by(email=email).first()
    
    if verify_email:
        flash('Email already exists')
        return redirect(url_for('auth.signup', **req))
    
    verify_username = User.query.filter_by(username=username).first()

    if verify_username:
        flash('User already exists')
        return redirect(url_for('auth.signup', **req))
    
    password = bcrypt.generate_password_hash(password).decode('utf-8')#generate password hash

    role = Role.query.filter_by(name=role).first()#search for the role
    
    new_user = User(username=username, email=email, password=password, role=role)#create object to insert into database

    #TODO: lookup for sqlalchemy exceptions, I spent a lot o time trying to figure out why the user wasn't being added, Shell would throw a clean exception
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        flash('Unable to register user, please try again later')
        return redirect(url_for('auth.signup', **req))
    
    flash('User created')
    return redirect(url_for('auth.signup'))
