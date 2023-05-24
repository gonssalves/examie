from flask import render_template, redirect, url_for, session
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

    all_questions = get_questions()
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
    form = QuestionForm(obj=question)

    if form.validate_on_submit():
        from models.auth import auth_edit_question
        return auth_edit_question(question)
    return render_template('edit_questions.html', form=form, question_id=question_id)


@main.route('/exams', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def exams():
    from models.entities import Exam, Question
    all_exams = Exam.show_all()

    if str(current_user.role) == 'Student':
        return render_template('exams_student.html', exams=all_exams)

    from forms import ExamForm

    all_questions = Question.show_all()
    form = ExamForm()

    if request.method == 'POST':
        from models.auth import auth_add_exam
        return auth_add_exam() 

    return render_template('exams.html', exams=all_exams, all_questions=all_questions, form=form)


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
    from models.entities import Exam
    from forms import ExamForm

    exam = Exam.show_one(exam_id)
    form = ExamForm(obj=exam)

    if form.validate_on_submit():
        from models.auth import auth_edit_exam
        return auth_edit_exam(exam)
    return render_template('edit_exams.html', form=form, exam_id=exam_id)


@main.route('/exams/<int:exam_id>/start', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def exams_start(exam_id):
    import datetime
    from models.entities import Exam, ExamQuestion
    from forms import QuestionForm

    opening_date = Exam.show_opening_date(exam_id)

    if not str(datetime.date.today()) == str(opening_date):
        flash('Exam is not open')
        return redirect(url_for('main.exams'))
    
    form = QuestionForm()

    exam = Exam.show_one(exam_id)
    exam_questions = ExamQuestion.query.filter_by(exam_id=exam_id).all()    

    #return str(exam)
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