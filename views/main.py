from flask import render_template, redirect, url_for
from flask import Blueprint, request, flash
from flask_login import login_required, current_user
from login_required import admin_login_required, admin_teacher_login_required
import time

#HERE THE VIEWS ARE CREATED
#VIEWS ARE FUNCTIONS RESPONSIBLE FOR HANDLING REQUESTS
#ASSIGNING A URL TO A VIEW GENERATES A ROUTE

#create blueprint
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')
 
@main.route('/questions', methods=['GET', 'POST'])
@login_required
@admin_teacher_login_required()
def questions():
    from cache import get_questions
    from forms import QuestionForm
    from models.entities import Question

    #all_questions = get_questions()
    all_questions = Question.show_all()

    form = QuestionForm()

    if request.method == 'POST':
        from models.auth import auth_add_question
        return auth_add_question()

    return render_template('questions.html', questions=all_questions, form=form)


@main.route('/questions/<int:question_id>/delete', methods=['GET'])
@login_required
@admin_teacher_login_required()
def delete_questions(question_id):
    from models.entities import Question

    question = Question.show_one(question_id)
  
    from models.auth import auth_delete_question
    return auth_delete_question(question)


@main.route('/questions/<int:question_id>', methods=['GET', 'POST'])
@login_required
@admin_teacher_login_required()
def edit_questions(question_id):
    from models.entities import Question
    from forms import QuestionForm

    question = Question.show_one(question_id)
    form = QuestionForm()

    if request.method == 'POST':
        from models.auth import auth_edit_question
        return auth_edit_question(question_id)
    return render_template('edit_questions.html', form=form, question_id=question_id, question=question)


@main.route('/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def exams():
    from models.entities import Exam, Question, SchoolClassStudent
    all_exams = Exam.show_all()

    class_id = SchoolClassStudent.show_class(current_user)
    
    classrooms = SchoolClassStudent.query.all()

    if str(current_user.role) == 'Student':
        return render_template('exams_student.html', exams=all_exams, user=current_user, classrooms=classrooms, class_id=class_id)

    from forms import ExamForm

    all_questions = Question.show_all()
    form = ExamForm()

    if request.method == 'POST':
        from models.auth import auth_add_exam
        return auth_add_exam() 

    return render_template('exams.html', exams=all_exams, all_questions=all_questions, form=form, user=current_user)


@main.route('/exams/<int:exam_id>/delete', methods=['GET'])
@login_required
@admin_teacher_login_required()
def delete_exams(exam_id):
    from models.entities import Exam

    exam = Exam.show_one(exam_id)
  
    from models.auth import auth_delete_exam
    return auth_delete_exam(exam)


@main.route('/exams/<int:exam_id>', methods=['GET', 'POST'])
@login_required
@admin_teacher_login_required()
def edit_exams(exam_id):
    from models.entities import Exam, Question
    from forms import ExamForm

    exam = Exam.show_one(exam_id)
    all_questions = Question.show_all()
    form = ExamForm()

    questions_id = exam.questions_id()

    if form.validate_on_submit():
        from models.auth import auth_edit_exam
        return auth_edit_exam(exam)
    return render_template('edit_exams.html', form=form, exam_id=exam_id, exam=exam, all_questions=all_questions, questions_id=questions_id)


@main.route('/exams/<int:exam_id>/start', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def exams_start(exam_id):
    import datetime
    from models.entities import Exam, ExamQuestion
    from forms import QuestionForm

    opening_date = Exam.show_opening_date(exam_id)

    
    
    form = QuestionForm()

    exam = Exam.show_one(exam_id)

    # if exam.status == 'closed':
    #     flash('Exam is not open')
    #     return redirect(url_for('main.exams'))
    # else:
    exam_questions = ExamQuestion.query.filter_by(exam_id=exam_id).all()    

    if request.method == 'POST':
        from models.auth import auth_start_exam
        return auth_start_exam(exam)
    return render_template('exam_start.html', exam=exam, exam_id=exam.id, exam_questions=exam_questions, form=form)


@main.route('/users', methods=['GET', 'POST'])
@login_required
@admin_login_required()
def users():
    from models.entities import User
    from forms import SignupForm

    all_users = User.show_all()
    form = SignupForm()

    if form.validate_on_submit():
        from models.auth import auth_signup
        return auth_signup() 
    return render_template('users.html', users=all_users, form=form)


@main.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_login_required()
def edit_users(user_id):
    from models.entities import User
    from forms import SignupForm

    user = User.show_one(user_id)
    form = SignupForm(obj=user)

    if form.validate_on_submit():
        from models.auth import auth_edit
        return auth_edit(user)
    return render_template('edit_users.html', form=form)


@main.route('/users/<int:user_id>/delete', methods=['GET'])
@login_required
@admin_login_required()
def delete_users(user_id):
    from models.entities import User

    user = User.show_one(user_id)
  
    from models.auth import auth_delete_user
    return auth_delete_user(user)

@main.route('/classes', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def classes():
    if str(current_user.role) == 'Student':
        return 'student'
        return render_template('classes_student.html')

    from models.entities import Exam, SchoolClass, User
    from forms import ClassroomForm

    form = ClassroomForm()

    all_exams = Exam.show_all()
    class_id = SchoolClass.show_class(current_user)
    classroom = SchoolClass.show_one(class_id)

    if form.validate_on_submit():
        from models.auth import auth_add_classroom
        return auth_add_classroom()

    return render_template('classes.html', exams=all_exams, user=current_user, class_id=class_id, classroom=classroom, User=User, form=form)

@main.route('/classes/<class_name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_teacher_login_required()
def classe(class_name):

    from models.entities import Exam, SchoolClass, User
    from forms import ClassroomForm

    all_exams = Exam.show_all()
    classroom = SchoolClass.show_one(class_name)
   
    return render_template('classe.html', class_name=class_name, exams=all_exams, user=current_user, classroom=classroom, User=User)


@main.route('/classes/<int:user_id>/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_teacher_login_required()
def student_exams(user_id):
    from models.entities import Exam, SchoolClass, User, StudentAnswer

    class_id = SchoolClass.show_class(current_user)
    student = User.show_one(user_id)
    all_exams = Exam.show_all()
    answers = StudentAnswer.query.all()

    exam_id = 0

    for answer in answers:
        if answer.user_id == student.id:
            exam_id = answer.exam_id
            
    print(exam_id)
    
    return render_template('student_exams.html', student=student, exams=all_exams, answers=answers, exam_id=exam_id)
    return 'aaaaa'

@main.route('/classes/<int:student_id>/exams/<int:exam_id>/done', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@admin_teacher_login_required()
def exams_done(student_id, exam_id):
    from models.entities import Exam, ExamQuestion, StudentAnswer
    from forms import QuestionForm
    form = QuestionForm()        

    exam = Exam.show_one(exam_id)

    answers = StudentAnswer.query.all()
    
    l=[]
    
    for answer in answers:
        if answer.exam_id == exam_id:
            l.append(answer.answerr)
    
    l = StudentAnswer.magic(exam_id=exam_id, question_id=answer.question_id)
    
    print(l) 
    
    #return 'fds?'

    exam_questions = ExamQuestion.query.filter_by(exam_id=exam_id).all()   

    return render_template('student_exams_done.html', exam_id=exam_id, student_id=student_id, form=form, exam_questions=exam_questions, answers=answers, l=l, StudentAnswer=StudentAnswer)
