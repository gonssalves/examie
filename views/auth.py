from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, logout_user

#create blueprint
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    ''' Login validation. '''
    from forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit(): #see that I'm not using request.methods explicitly  
        from models.auth import auth_login
        return auth_login()
    form.process(request.args)
    return render_template('login.html', form=form)
        
@auth.route('/signup', methods=['GET', 'POST'])
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

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect((url_for('auth.login')))

@auth.route('/account-recovery', methods=['GET', 'POST'])
def account_recovery():
    from forms import AccountRecoveryForm
    form = AccountRecoveryForm()
    if form.validate_on_submit():
        from models.auth import auth_recovery
        return auth_recovery()
    return render_template('password.html', form=form)

@auth.route('/password-reset', methods=['GET', 'POST'])
@login_required
def password_reset():
    from forms import PasswordResetForm
    form = PasswordResetForm()
    if form.validate_on_submit():
        from models.auth import auth_reset
        return auth_reset()
    return render_template('first_access.html', form=form)
