import json

from models import Question, Choice, create_database_session

session = create_database_session()
session.query(Question).delete()
session.query(Choice).delete()

with open('data.json') as file:
    data = json.load(file)
    for question_text, choice_data in data.items():
        question = Question(question_text=question_text)
        for choice_text, votes in choice_data.items():
            choice = Choice(choice_text=choice_text, votes=votes)
            question.choices.append(choice)
        session.add(question)
    session.commit()

questions = session.query(Question).all()

for question in questions:
    choices = ', '.join([f'{choice.choice_text}({choice.votes})'
                         for choice in question.choices])
    print(f'{question.question_text}: {choices}')
