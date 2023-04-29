from app import db
from flask_login import UserMixin
from app import bcrypt

class Role(db.Model):
    #create the role table
    #define the users types
    #TODO: User this table for authentication purposes
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role') #TODO: Search about the relationships

    #print role name
    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model, UserMixin):
    #create the user table
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def verify_password(self, password):
        ''' Use hashing to verify if the password passed through form is correct'''
        pw_hash = bcrypt.generate_password_hash(password)
        return bcrypt.check_password_hash(pw_hash, self.password)        
    
    #print user name
    def __repr__(self):
        return f'<User {self.username}>'