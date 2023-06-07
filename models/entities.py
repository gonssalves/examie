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
    real_name = db.Column(db.String())
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(), nullable=False)
    first_access = db.Column(db.Boolean(), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    questions = db.relationship('Question', backref='user')
    exams = db.relationship('Exam', backref='user')
    student_answers = db.relationship('StudentAnswer', backref='user')
    classrooms = db.relationship('SchoolClass', backref='user')
    classroom_student = db.relationship('SchoolClassStudent', backref='user')
    student_grades = db.relationship('StudentGrade', backref='user')

    def __repr__(self):
        return f'{self.username}'
    
    @staticmethod
    def show_all():
        ''' Return all the users '''
        return User.query.all()
    
    @staticmethod
    def show_one(user_id):
        return User.query.get(int(user_id))
    
    # def get_student(self):

    
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
    
    def delete_tags(self):
        for tag in self.tags:
            db.session.delete(tag)
        db.session.commit()
    
    def get_answer_tf(self):
        for answer in self.answers:
            if answer.question_id == self.id:
                return bool(answer.correct)
            
    def get_answer_sc_mc(self):
        l_answer = []
        l_sc = []
        l_mc = []
        l_ids = []

        i = 0

        for answer in self.answers:
            if answer.question_id == self.id:
                i += 1
                l_ids.append(answer.id)
                l_answer.append(answer.answerr)
                temp = str(answer.correct)
                l_mc.append(temp.lower())
                if answer.correct == True:
                    l_sc.append(f'Answer{i}')
        
        l_all = [l_answer, l_sc, l_mc, l_ids]

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
    student_answerss = db.relationship('StudentAnswer', backref='exam')
    classes_exams = db.relationship('SchoolClassExam', backref='exam')
    
    @staticmethod
    def show_one(exam_id):
        x = Exam.query.get(int(exam_id))
        return Exam.query.get(int(exam_id))
    
    @staticmethod
    def show_opening_date(exam_id):
        exam =  Exam.query.get(int(exam_id))
        return exam.opening_date
    
    @staticmethod
    def show_all():
        ''' Return all the questions '''
        return Exam.query.all()
    
    def questions_id(self):
        questions = Question.show_all()
        
        questions_id = []

        for e_q in self.exam_questions:
            for question in questions:
                if question.id == e_q.question_id:
                    questions_id.append(question.id)
        
        return questions_id
    
class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    
    exam = db.relationship('Exam', back_populates='exam_questions')

    def __repr__(self):
        return f'{self.exam_id} {self.question_id}'

class StudentAnswer(db.Model):
    __tablename__ = 'student_answers'
    id = db.Column(db.Integer, primary_key=True)
    answerr = db.Column(db.String(), nullable=False)
    correct = db.Column(db.String())
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def magic(exam_id, question_id):
        answers = StudentAnswer.query.all()

        l = {}
        for answer in answers:
            if answer.exam_id == exam_id and  answer.question_id == question_id:
                key = answer.answerr
                l[key] = answer.correct
            
        return l

class SchoolClass(db.Model):
    __tablename__ = 'school_classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    invite_code = db.Column(db.String(), nullable=False)
    creation_date = db.Column(db.Date, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    school_class_students = db.relationship('SchoolClassStudent', backref='schol_classes')

    def show_class(user):
        all = SchoolClass.query.all()
        for i in all:
            if i.teacher_id == user.id:
                print(i)
                return int(i.id)
        return 'aaa'
    
    def show_one(class_name):
        return SchoolClass.query.filter_by(name=class_name).first()

    
class SchoolClassStudent(db.Model):
    __tablename__ = 'school_classes_students'
    id = db.Column(db.Integer, primary_key=True)
    school_class_id = db.Column(db.Integer, db.ForeignKey('school_classes.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'{self.school_class_id}|'
    
    def show_class(user):
        all = SchoolClassStudent.query.all()
        for i in all:
            if i.student_id == user.id:
                return int(i.id)
        return 'aaa'
    
class SchoolClassExam(db.Model):
    __tablename__ = 'school_classes_exams'
    id = db.Column(db.Integer, primary_key=True)
    school_class_id = db.Column(db.Integer, db.ForeignKey('school_classes.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))

    def __repr__(self):
        return f'{self.school_class_id}'

class StudentGrade(db.Model):
    __tablename__ = 'student_grades'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String())
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))