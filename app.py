import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from controller import controller as controller_blueprint
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

#create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ayofumylu'

#configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create extensions
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#define the log in view and help prevent user's sessions from being stolen
login_manager.login_view = 'controller.login' 
login_manager.session_protection = 'strong' #each request generates and identifier for the user's computer

@login_manager.user_loader
def load_user(user_id):
    ''' Reload the user object from the user ID stored in the session. '''
    from models.entities import User
    return User.query.get(int(user_id))

#register the blueprint (blueprints handles the routes) 
app.register_blueprint(controller_blueprint, url_prefix='')