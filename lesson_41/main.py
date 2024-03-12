from fastapi import FastAPI, HTTPException

from data import *
from models import Question, create_database_session

app = FastAPI()
db = create_database_session()


@app.get("/questions")
def get_questions(ordering: str = '-pub_date',
                  page_size: int = 5,
                  page: int = 1) -> PaginatedQuestionsData:
    order_by = None
    if ordering == 'question_text':
        order_by = Question.question_text
    elif ordering == '-question_text':
        order_by = Question.question_text.desc()

    questions = db.query(Question).order_by(order_by)[(page - 1) * page_size: page * page_size]
    results = [serialize_question(question) for question in questions]
    return PaginatedQuestionsData(count=len(questions), results=results)


@app.get("/questions/{question_id}", responses={404: {}})
def get_question(question_id: int) -> QuestionData:
    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404,
                            detail=f'Question with id {question_id} does not exist')
    return serialize_question(question)


class QuestionVote(BaseModel):
    choice_id: int


@app.post('/questions/{question_id}/vote', responses={404: {}})
def vote_question(question_id: int, question_vote: QuestionVote) -> QuestionData:
    question: Question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404,
                            detail=f'Question with id {question_id} does not exist')

    for choice in question.choices:
        if choice.id == question_vote.choice_id:
            choice.votes += 1
            return serialize_question(question)

    raise HTTPException(status_code=404,
                        detail=f'Question {question_id} does not have choice '
                               f'with id {question_vote.choice_id}')
