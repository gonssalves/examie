from app import cache
import time

@cache.cached(timeout=60)
def get_questions():
    from models.entities import Question

    # Verifica se as questões estão armazenadas em cache
    if cache.get('questions'):
        # Questões em cache, retorna imediatamente
        return cache.get('questions')
    
    # Questões não estão em cache, cria um atraso de 5 segundos
    time.sleep(5)
    
    # Lógica para buscar as questões do banco de dados
    questions = Question.query.all()

    for question in questions:
        question.user
    
    # Armazena as questões em cache
    cache.set('questions', questions)
    
    return questions
