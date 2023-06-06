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
    exams = db.relationship('Exam', backref='user')

    def __repr__(self):
        return f'{self.username}'
    
    @staticmethod
    def show_all():
        ''' Return all the users '''
        return User.query.all()
    
    @staticmethod
    def show_one(user_id):
        return User.query.get(int(user_id))
    
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
    exam_questions_rel = db.relationship('ExamQuestion', backref='question_rel')    # tags = db.relationship('Tag', backref='question')
    # answers = db.relationship('Answer', backref='question')
    # exam_questions = db.relationship('ExamQuestion', backref='question_rel')

    def __repr__(self):
        return f'{self.theme}'
    
    @staticmethod
    def show_one(question_id):
        return Question.query.get(int(question_id))
    
    @staticmethod
    def show_all():
        ''' Return all the questions '''
        return Question.query.all()
    
    def get_tags(self):
        temp = ''
        for tag in self.tags:
            temp += str(tag) + ' '
        return temp
    
    def get_answer_tf(self):
        for answer in self.answers:
            if answer.question_id == self.id:
                return bool(answer.correct)
            
    def get_answer_sc_mc(self):
        l_answer = []
        l_sc = []
        l_mc = []

        i = 0

        for answer in self.answers:
            if answer.question_id == self.id:
                i += 1
                l_answer.append(answer.answerr)
                temp = str(answer.correct)
                l_mc.append(temp.lower())
                if answer.correct == True:
                    l_sc.append(f'Answer{i}')
        
        l_all = [l_answer, l_sc, l_mc]

        return l_all
    
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
    correct = db.Column(db.Boolean(), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    # def __repr__(self):
    #     return f'{self.answerr} | {self.question_id}'
    
class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.Date(), nullable=False)
    opening_date = db.Column(db.Date, nullable=False)
    execution_time = db.Column(db.Integer, nullable=False)
    questions_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    exam_questions = db.relationship('ExamQuestion', back_populates='exam')     
    
    @staticmethod
    def show_one(exam_id):
        x = Exam.query.get(int(exam_id))
        print(x.exam_questions)
        return Exam.query.get(int(exam_id))
    
    @staticmethod
    def show_opening_date(exam_id):
        exam =  Exam.query.get(int(exam_id))
        return exam.opening_date
    
    @staticmethod
    def show_all():
        ''' Return all the questions '''
        return Exam.query.all()
    
class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    
    exam = db.relationship('Exam', back_populates='exam_questions')

    def __repr__(self):
        return f'{self.exam_id} {self.question_id}'
