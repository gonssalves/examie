from models.entities import User, Role, Answer, Tag, Question, Exam, ExamQuestion, StudentAnswer
from flask import request, redirect, url_for, flash, session
from flask_login import login_user, current_user
from app import db, bcrypt, mail, cache
from email_validator import validate_email, EmailNotValidError
from email.message import EmailMessage
import smtplib
import ssl
import string
import secrets
import datetime


def generate_password():
    letters = string.ascii_letters
    digits = string.digits
    especial_characters = string.punctuation
    size = 8

    alphabet = letters + digits + especial_characters
    
    random_password = ''

    for i in range(size):
        random_password += f'{secrets.choice(alphabet)}'
    
    return random_password

def check_email(email, route):

    req = request.form.copy()
    if 'password' in req: 
        req.pop('password')
    req.pop('csrf_token')
    req.pop('submit')

    try:
        emailinfo = validate_email(email, check_deliverability=True)#check_deliverability DNS queries are made to check that the domain name in the email address (the part after the @-sign) can receive mail
        email = emailinfo.normalized#
        return email
    except EmailNotValidError as e:
        flash(str(e))
        return redirect(url_for(route, **req))
    
def send_email(email, subject, body):
        email_sender = 'contacttrepverter@gmail.com'
        email_password = 'ipxtsyzonfvriiem'
        email_receiver = email

        #Set the subject and body of the email
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        
        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            return 'idk'
        
def auth_login():
    ''' Check if the user exists in the database and if the information submitted is correct.'''
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = (True if request.form.get('remember_me') else False)
    
    #check if user is on the database
    user = User.query.filter_by(username=username).first()#returns none if there's no such user

    #pop password from the request body
    req = request.form.copy()
    req.pop('password')
    req.pop('csrf_token')
    req.pop('submit')

    if not user:
        flash('Invalid username or password.')
        return redirect(url_for('auth.login', **req))#**req is used to sent the request to the form, so the user doesn't need to type everything again
        
    if not user.verify_password(password) or password == user.password:
        flash('Invalid username or password.')
        return redirect(url_for('auth.login', **req))
    
    if user.first_access:
            login_user(user, remember=remember_me)
            return redirect(url_for('auth.password_reset'))
    login_user(user, remember=remember_me)#once user is authenticated, he is logged with this function | remember-me can keep the user logged after the browser is closed
    return redirect(request.args.get('next') or url_for('main.index'))
    #TODO: search about this url_for parameters

def auth_reset():
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if password != password2:
        flash('Passwords must be the same')
        return redirect(url_for('auth.password_reset'))
    
    user = current_user

    try:
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.first_access = False
        db.session.commit()
    except:
        flash('Unable to alter password, please try again later')
        return redirect(url_for('auth.password_reset'))
    
    flash('Password changed')
    return redirect(url_for('main.index'))
    
def auth_recovery():
    email = request.form.get('email')

    req = request.form.copy()
    req.pop('csrf_token')
    req.pop('submit')

    email = check_email(email, 'auth.recovery')
    
    user = User.query.filter_by(email=email).first()

    if user:
        password = user.password
        subject = 'Recovery Account'
        body = f'Use this password to log in: {password}'

        send_email(email=email, subject=subject, body=body)

    flash('If this email is registered, you received a message. Check your spam box.')
    return redirect(url_for('auth.account_recovery'))

def auth_signup():
    ''' Validate the informations sent and register an user. '''
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')

    verify_username = User.query.filter_by(username=username).first()

    if verify_username:
        flash('User already exists')
        return redirect(url_for('main.users'))
    
    email = check_email(email=email, route='main.users')
    
    verify_email = User.query.filter_by(email=email).first()
    
    if verify_email:
        flash('Email already exists')
        return redirect(url_for('main.users'))
    
    random_password = generate_password()

    password = bcrypt.generate_password_hash(random_password).decode('utf-8')#generate password hash

    role = Role.query.filter_by(name=role).first()#search for the role
    
    new_user = User(username=username, email=email, password=password, first_access = True, role=role)#create object to insert into database

    #TODO: lookup for sqlalchemy exceptions, I spent a lot o time trying to figure out why the user wasn't being added, Shell would throw a clean exception
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        flash('Unable to register user, please try again later')
        return redirect(url_for('main.users'))
    
    subject = 'Account Created'
    body = f'Your account has been created.\n Login: {username} \n Password: {random_password}'
    send_email(email, subject, body)

    flash('User created')
    return redirect(url_for('main.users'))


def auth_edit(old_user):
    username = request.form.get('username')
    email = request.form.get('email')
    role = request.form.get('role')
    
    verify_username = User.query.filter_by(username=username).first()

    if verify_username:
        if verify_username.id != old_user.id:
            flash('User already exists')
            return redirect(url_for('main.users'))
    
    email = check_email(email=email, route='main.users')
    
    verify_email = User.query.filter_by(email=email).first()
    
    if verify_email:
        if verify_email.id != old_user.id:
            flash('Email already exists')
            return redirect(url_for('main.users'))
    
    role = Role.query.filter_by(name=role).first()#search for the role
    

    edit_user = old_user

    edit_user.username=username
    edit_user.email=email
    edit_user.role=role

    try:
        db.session.add(edit_user)
        db.session.commit()
    except:
        flash('Unable to alter user, please try again later')
        return redirect(url_for('main.users'))
    
    flash('User altered')
    return redirect(url_for('main.users'))

def auth_delete_user(old_user):
    try:
        db.session.delete(old_user)
        db.session.commit()
    except:
        flash('Unable to delete user, please try again later')
        return redirect(url_for('main.users'))
    
    flash('User deleted')
    return redirect(url_for('main.users'))

def auth_add_question():
    subject = request.form.get('subject')
    theme = request.form.get('theme')
    description = request.form.get('description')
    level = request.form.get('level')
    tags = request.form.get('tags')
    answer_type = request.form.get('answer_type')
    tags = request.form.get('tags')
    list_tags = tags.split()
 
    creation_date = datetime.date.today()

    new_question = Question(subject=subject, theme=theme, description=description, level=level, answer_type=answer_type, creation_date=creation_date, user_id=current_user.id)

    for tag in list_tags:
        new_tag = Tag(tag_name=tag, question=new_question)
        db.session.add(new_tag)

    if answer_type == 'op':
        db.session.add(new_question)
        db.session.commit()
    elif answer_type == 'mc':
        answer1 = request.form.get('answer1')
        answer2 = request.form.get('answer2')
        answer3 = request.form.get('answer3')
        answer4 = request.form.get('answer4')

        answer1_correct = (True if 'multiple_right_answer1' in request.form else False)
        answer2_correct = (True if 'multiple_right_answer2' in request.form else False)
        answer3_correct = (True if 'multiple_right_answer3' in request.form else False)
        answer4_correct = (True if 'multiple_right_answer4' in request.form else False)
        
    
        new_answer1 = Answer(answerr=answer1, correct=answer1_correct, question=new_question)
        new_answer2 = Answer(answerr=answer2, correct=answer2_correct, question=new_question)
        new_answer3 = Answer(answerr=answer3, correct=answer3_correct, question=new_question)
        new_answer4 = Answer(answerr=answer4, correct=answer4_correct, question=new_question)

        try:
            db.session.add_all([new_question, new_answer1, new_answer2, new_answer3, new_answer4])
            db.session.commit()
        except:
            print('here1')

            flash('Unable to add question, please try again later')
            return redirect(url_for('main.questions'))
        
    elif answer_type == 'sc':
        answer1 = request.form.get('answer1')
        answer2 = request.form.get('answer2')
        answer3 = request.form.get('answer3')
        answer4 = request.form.get('answer4')
        
        single_right_answer = request.form.get('single_right_answer')

        answer1_correct = (True if 'Answer1' in single_right_answer else False)
        answer2_correct = (True if 'Answer2' in single_right_answer else False)
        answer3_correct = (True if 'Answer3' in single_right_answer else False)
        answer4_correct = (True if 'Answer4' in single_right_answer else False)

        new_answer1 = Answer(answerr=answer1, correct=answer1_correct, question=new_question)

        new_answer2 = Answer(answerr=answer2, correct=answer2_correct, question=new_question)

        new_answer3 = Answer(answerr=answer3, correct=answer3_correct, question=new_question)

        new_answer4 = Answer(answerr=answer4, correct=answer4_correct, question=new_question)

        try:
            db.session.add_all([new_question, new_answer1, new_answer2, new_answer3, new_answer4])
            db.session.commit()
        except:
            print('here2')

            flash('Unable to add question, please try again later')
            return redirect(url_for('main.questions'))

    elif answer_type == 'tf':
        true_or_false_answer = (True if request.form.get('true_or_false_answer') == 'True' else False)
    
        new_answer = Answer(answerr='tf', correct=true_or_false_answer, question=new_question)

        try:
            db.session.add_all([new_question, new_answer])
            db.session.commit()
        except:
            print('here3')
            flash('Unable to add question, please try again later')
            return redirect(url_for('main.questions'))

    cache.clear()
    flash('Question created')
    return redirect(url_for('main.questions'))

def auth_delete_question(old_question):
    try:
        db.session.delete(old_question)
        db.session.commit()
    except:
        flash('Unable to delete question, please try again later')
        return redirect(url_for('main.questions'))
    
    cache.clear()
    flash('Question deleted')
    return redirect(url_for('main.questions'))

def auth_edit_question(old_question_id):
    print(str(request.form), '\n')
    subject = request.form.get('subject')
    theme = request.form.get('theme')
    description = request.form.get('description')
    level = request.form.get('level')
    answer_type = request.form.get('answer_type')
    tags = request.form.get('tags')

    list_tags = tags.split()

    old_question = Question.query.get(int(old_question_id))

    old_question.subject = subject
    old_question.theme = theme
    old_question.description = description
    old_question.level = level
    
    if old_question.get_tags() != tags:
        for tag in list_tags:
            new_tag = Tag(tag_name=tag, question=old_question)
            db.session.add(new_tag)
        old_question.delete_tags()
    
    if answer_type == 'mc': 
        answer1 = request.form.get('answer1')
        answer2 = request.form.get('answer2')
        answer3 = request.form.get('answer3')
        answer4 = request.form.get('answer4')

        answer1_correct = (True if request.form.get('multiple_right_answer1') else False)
        answer2_correct = (True if request.form.get('multiple_right_answer2') else False)
        answer3_correct = (True if request.form.get('multiple_right_answer3') else False)
        answer4_correct = (True if request.form.get('multiple_right_answer4') else False)

        if answer_type == old_question.answer_type:
            answers = old_question.get_answer_sc_mc()
            answers_temp = [answer1, answer2, answer3, answer4]
            
            answer_1 = Answer.query.get(int(answers[3][0]))
            answer_2 = Answer.query.get(int(answers[3][1]))
            answer_3 = Answer.query.get(int(answers[3][2]))
            answer_4 = Answer.query.get(int(answers[3][3]))

            if answers[0] == answers_temp:
                answer_1.correct = answer1_correct
                answer_2.correct = answer2_correct
                answer_3.correct = answer3_correct
                answer_4.correct = answer4_correct

            else:
                answer_1.answerr = answer1
                answer_2.answerr = answer2
                answer_3.answerr = answer3
                answer_4.answerr = answer4
                
                answer_1.correct = answer1_correct
                answer_2.correct = answer2_correct
                answer_3.correct = answer3_correct
                answer_4.correct = answer4_correct

            db.session.add_all([answer_1, answer_2, answer_3, answer_4])
        else:
            new_answer1 = Answer(answerr=answer1, correct=answer1_correct, question=old_question)
            new_answer2 = Answer(answerr=answer2, correct=answer2_correct, question=old_question)
            new_answer3 = Answer(answerr=answer3, correct=answer3_correct, question=old_question)
            new_answer4 = Answer(answerr=answer4, correct=answer4_correct, question=old_question)

            db.session.add_all([new_answer1, new_answer2, new_answer3, new_answer4])

    elif answer_type == 'sc':
        answer1 = request.form.get('answer1')
        answer2 = request.form.get('answer2')
        answer3 = request.form.get('answer3')
        answer4 = request.form.get('answer4')

        answer_sc = request.form.get('single_right_answer')

        answer1_correct = (True if answer_sc == 'Answer1' else False)
        answer2_correct = (True if answer_sc == 'Answer2' else False)
        answer3_correct = (True if answer_sc == 'Answer3' else False)
        answer4_correct = (True if answer_sc == 'Answer4' else False)

        if answer_type == old_question.answer_type:
            answers = old_question.get_answer_sc_mc()
            
            answer_1 = Answer.query.get(int(answers[3][0]))
            answer_2 = Answer.query.get(int(answers[3][1]))
            answer_3 = Answer.query.get(int(answers[3][2]))
            answer_4 = Answer.query.get(int(answers[3][3]))

            answers_temp = [answer1, answer2, answer3, answer4]
            
            if answers[0] == answers_temp:
                answer_1.correct = answer1_correct
                answer_2.correct = answer2_correct
                answer_3.correct = answer3_correct
                answer_4.correct = answer4_correct

            else:
                answer_1.answerr = answer1
                answer_2.answerr = answer2
                answer_3.answerr = answer3
                answer_4.answerr = answer4
                
                answer_1.correct = answer1_correct
                answer_2.correct = answer2_correct
                answer_3.correct = answer3_correct
                answer_4.correct = answer4_correct

            db.session.add_all([answer_1, answer_2, answer_3, answer_4])

        else:
            new_answer1 = Answer(answerr=answer1, correct=answer1_correct, question=old_question)
            new_answer2 = Answer(answerr=answer2, correct=answer2_correct, question=old_question)
            new_answer3 = Answer(answerr=answer3, correct=answer3_correct, question=old_question)
            new_answer4 = Answer(answerr=answer4, correct=answer4_correct, question=old_question)

            db.session.add_all([new_answer1, new_answer2, new_answer3, new_answer4])


    elif answer_type == 'tf':
        true_or_false_answer = (True if request.form.get('true_or_false_answer') == 'True' else False)
    
        answers = old_question.get_answer_sc_mc()
        
        if answer_type == old_question.answer_type:
            answer_id = str(answers[3][0])

            answer = Answer.query.get(int(answer_id))
            answer.correct = true_or_false_answer

            db.session.add(answer)

        else:
            new_answer = Answer(answerr='tf', correct=true_or_false_answer, question=old_question)
            db.session.add(new_answer)


    old_question.answer_type = answer_type

    #return 'foda-se?'

    db.session.add(old_question)    
    db.session.commit()

    flash('Question modified')
    return redirect(url_for('main.questions'))
    
def auth_add_exam():
    if not 'question_id' in request.form:
        req = request.form.copy()
        req.pop('csrf_token')

        flash('Select at least one question')
        return redirect(url_for('main.exams', **req))   
    
    opening_date = request.form.get('opening_date')
    execution_time = request.form.get('execution_time')
    questions = request.form.getlist('question_id')
    questions_amount = len(questions)

    creation_date = datetime.date.today()

    opening_date = datetime.datetime.strptime(opening_date, '%Y-%m-%d').date()

    new_exam = Exam(creation_date=creation_date, opening_date=opening_date, execution_time=execution_time, questions_amount=questions_amount, user_id=current_user.id)
    
    for question in questions:
        new_exam_question = ExamQuestion(exam=new_exam, question_id=int(question))
        db.session.add(new_exam_question)

    try:
        db.session.add_all([new_exam, new_exam_question])
    except:
        flash('Unable to create exam, please try again later')
        return redirect(url_for('main.exams'))
    
    db.session.commit()
    flash('Exam created')
    return redirect(url_for('main.exams'))

    return str(questions)

def auth_delete_exam(old_exam):
    try:
        db.session.delete(old_exam)
        db.session.commit()
    except:
        flash('Unable to delete exam, please try again later')
        return redirect(url_for('main.exams'))
    
    flash('Exam deleted')
    return redirect(url_for('main.exams'))

def auth_edit_exam(old_exam):
    print(request.form, '/n\n')
    if not 'question_id' in request.form:
        req = request.form.copy()
        req.pop('csrf_token')

        flash('Select at least one question')
        return redirect(url_for('main.exams', **req)) 

    opening_date = request.form.get('opening_date')
    execution_time = request.form.get('execution_time')
    questions_id = request.form.getlist('question_id')
    
    questions_amount = len(questions_id)

    opening_date = datetime.datetime.strptime(opening_date, '%Y-%m-%d').date()

    old_exam.opening_date = opening_date
    old_exam.execution_time = execution_time
    old_exam.questions_amount = questions_amount
    
    
    all_exam_questions = ExamQuestion.query.all()
    
    for exam_question in all_exam_questions:
        if exam_question.exam_id == old_exam.id:
            db.session.delete(exam_question)

    for idd in questions_id:
        new_exam_question = ExamQuestion(exam=old_exam, question_id=int(idd))
        db.session.add(new_exam_question)
    
    try:
        db.session.commit()
    except:
        flash('Unable to modify exam, please try again later')
        return redirect(url_for('main.exams'))
    
    flash('Exam modified')
    return redirect(url_for('main.exams'))

def auth_start_exam(exam):
    temp = request.form.getlist('multiple_right_answer')
    request_copy = request.form.copy()

    request_copy.pop('csrf_token')
    request_copy.pop('submit')

    for k, v in request.form.items():
        if k == 'csrf_token' or k == 'submit':
            pass
        else:
            #print(key, value)
            new_student_answer = StudentAnswer(answerr=v, exam_id=exam.id, user_id=current_user.id)
            db.session.add(new_student_answer)


    db.session.commit()


    return 'tô doido, tô doido'
    
    flash('Exam sended')
    return redirect(url_for('main.exams'))
