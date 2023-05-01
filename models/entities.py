from app import db
from flask_login import UserMixin
from app import bcrypt

class Role(db.Model):
    #create the role table
    #define the users types
    #TODO: Use this table for authentication purposes
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role') #TODO: Search about the relationships

    #define how Role.query.all() will be print
    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model, UserMixin):
    #create the user table
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def verify_password(self, password):
        ''' Use hashing to verify if the password passed through form is correct'''
        return bcrypt.check_password_hash(self.password, password)       
    
    def __repr__(self):
        return f'<User {self.username}>'