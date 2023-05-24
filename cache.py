from app import cache
import time

@cache.cached(timeout=60)
def get_questions():
    from models.entities import Question

    # verify if the questions are store are cached
    if cache.get('questions'):
        # questions are cached, returns immediately
        return cache.get('questions')
    
    # questions are not cached, creates a 5 seconds delay
    #time.sleep(5)
    
    # get the questions from the database
    questions = Question.show_all()

    for question in questions:
        question.user
    
    # Armazena as questões em cache
    cache.set('questions', questions)
    
    return questions
