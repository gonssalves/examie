from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mailing import Mail
from views.main import main as view_main
from views.error import error as view_error
from views.auth import auth as view_auth
from flask_caching import Cache
import os

basedir = os.path.abspath(os.path.dirname(__file__))

from secret import SECRET_KEY, MY_EMAIL, MY_PASSWORD

#create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

#configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = MY_EMAIL
app.config['MAIL_PASSWORD'] = MY_PASSWORD
app.config['MAIL_TLS'] = True
app.config['MAIL_SSL'] = False

#create extensions
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

#define the log in view and help prevent user's sessions from being stolen
login_manager.login_view = 'auth.login' 
login_manager.session_protection = 'strong' #each request generates and identifier for the user's computer

@login_manager.user_loader
def load_user(user_id):
    ''' Reload the user object from the user ID stored in the session. '''
    from models.entities import User
    return User.query.get(int(user_id))

#register the blueprint (blueprints handles the routes) 
app.register_blueprint(view_main)
app.register_blueprint(view_error)
app.register_blueprint(view_auth)
