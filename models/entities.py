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
    users = db.relationship('User', backref='role')

    #define how Role.query.all() will be print
    def __repr__(self):
        return f'{self.name}'

class User(db.Model, UserMixin):
    #create the user table
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(), nullable=False)
    first_access = db.Column(db.Boolean(), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    questions = db.relationship('Question', backref='user')
    exam = db.relationship('Exam', backref='user')

    def __repr__(self):
        return f'{self.username}'
    
    def show_all():
        ''' Return all the users '''
        return User.query.all()
    
    def verify_password(self, password):
        ''' Use hashing to verify if the password passed through form is correct'''
        return bcrypt.check_password_hash(self.password, password)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64), nullable=False, index=True)
    theme = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(), nullable=False)
    level = db.Column(db.String(), nullable=False)
    answer_type = db.Column(db.String(20), nullable=False)
    creation_date = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    tags = db.relationship('Tag', backref='question')
    answers = db.relationship('Answer', backref='question')
    questions_exam = db.relationship('ExamQuestion', backref='question')

    def __repr__(self):
        return f'{self.theme}'
    
    def show_all():
        ''' Return all the questions '''
        return Question.query.all()
    
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __repr__(self):
        return f'{self.tag_name}'
    
class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    answerr = db.Column(db.String(), nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    
class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.Date(), nullable=False)
    opening_time = db.Column(db.String(10), nullable=False)
    closing_time = db.Column(db.String(10), nullable=False)
    execution_time = db.Column(db.Integer, nullable=False)
    questions_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    exam_questions = db.relationship('ExamQuestion', backref='exam')

class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
