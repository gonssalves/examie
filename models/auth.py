from models.entities import User, Role
from flask import request, redirect, url_for, flash, session
from flask_login import login_user, current_user
from app import db, bcrypt, mail
from email_validator import validate_email, EmailNotValidError
from email.message import EmailMessage
import smtplib
import ssl
import string
import secrets

def generate_password():
    letters = string.ascii_letters
    digits = string.digits
    especial_characters = string.punctuation
    size = 8

    alphabet = letters + digits + especial_characters
    
    random_password = ''

    for i in range(size):
        random_password += f'{secrets.choice(alphabet)}'
    
    return random_password

def check_email(email, route):

    req = request.form.copy()
    if 'password' in req: 
        req.pop('password')
    req.pop('csrf_token')
    req.pop('submit')

    try:
        emailinfo = validate_email(email, check_deliverability=True)#check_deliverability DNS queries are made to check that the domain name in the email address (the part after the @-sign) can receive mail
        email = emailinfo.normalized#
        return email
    except EmailNotValidError as e:
        flash(str(e))
        return redirect(url_for(route, **req))
    
def send_email(email, subject, body):
        email_sender = 'contacttrepverter@gmail.com'
        email_password = 'ipxtsyzonfvriiem'
        email_receiver = email

        #Set the subject and body of the email
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
            return 'idk'
        
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

    if not user:
        flash('Invalid username or password.')
        return redirect(url_for('auth.login', **req))#**req is used to sent the request to the form, so the user doesn't need to type everything again
        
    if not user.verify_password(password) or password == user.password:
        flash('Invalid username or password.')
        return redirect(url_for('auth.login', **req))
    
    if user.first_access:
            login_user(user, remember=remember_me)
            return redirect(url_for('auth.password_reset'))
    login_user(user, remember=remember_me)#once user is authenticated, he is logged with this function | remember-me can keep the user logged after the browser is closed
    return redirect(request.args.get('next') or url_for('main.index'))
    #TODO: search about this url_for parameters

def auth_reset():
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if password != password2:
        flash('Passwords must be the same')
        return redirect(url_for('auth.password_reset'))
    
    user = current_user

    try:
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.first_access = False
        db.session.commit()
    except:
        flash('Unable to alter password, please try again later')
        return redirect(url_for('auth.password_reset'))
    
    flash('Password changed')
    return redirect(url_for('main.index'))
    
def auth_recovery():
    email = request.form.get('email')

    req = request.form.copy()
    req.pop('csrf_token')
    req.pop('submit')

    email = check_email(email, 'auth.recovery')
    
    user = User.query.filter_by(email=email).first()

    if user:
        password = user.password
        subject = 'Recovery Account'
        body = f'Use this password to log in: {password}'

        send_email(email=email, subject=subject, body=body)

    flash('If this email is registered, you received a message. Check your spam box.')
    return redirect(url_for('auth.account_recovery'))

def auth_signup():
    ''' Validate the informations sent and register an user. '''
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')

    req = request.form.copy()
    req.pop('csrf_token')
    req.pop('submit')

    email = check_email(email=email, route='auth.signup')
    
    verify_email = User.query.filter_by(email=email).first()
    
    if verify_email:
        flash('Email already exists')
        return redirect(url_for('auth.signup', **req))
    
    verify_username = User.query.filter_by(username=username).first()

    if verify_username:
        flash('User already exists')
        return redirect(url_for('auth.signup', **req))
    
    random_password = generate_password()

    password = bcrypt.generate_password_hash(random_password).decode('utf-8')#generate password hash

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
