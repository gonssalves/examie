import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from controllers.main import main as main_blueprint
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

#create the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ayofumylu'

#configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create extensions
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#define the log in view and help prevent user's sessions from being stolen
login_manager.login_view = 'main.login' 
login_manager.session_protection = 'strong' #each request generates and identifier for the user's computer

@login_manager.user_loader
def load_user(user_id):
    ''' Reload the user object from the user ID stored in the session. '''
    from models.entities import User
    return User.query.get(int(user_id))

#register the blueprint (blueprints handles the routes) 
app.register_blueprint(main_blueprint, url_prefix='')