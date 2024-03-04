from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from polls_models import Database, PaginatedQuestions, Question

app = FastAPI()
db = Database()


@app.get("/questions")
def get_questions(ordering: str = '-pub_date',
                  page_size: int = 5,
                  page: int = 1) -> PaginatedQuestions:
    # TODO implement ordering
    questions = db.get_questions()[(page - 1) * page_size: page * page_size]
    return PaginatedQuestions(count=len(questions), results=questions)


@app.get("/questions/{question_id}", responses={404: {}})
def get_question(question_id: int) -> Question:
    question = db.get_question(question_id)
    if question is None:
        raise HTTPException(status_code=404,
                            detail=f'Question with id {question_id} does not exist')
    return question


class QuestionVote(BaseModel):
    choice_id: int


@app.post('/questions/{question_id}/vote', responses={404: {}})
def vote_question(question_id: int, question_vote: QuestionVote) -> Question:
    question: Question = db.get_question(question_id)
    if question is None:
        raise HTTPException(status_code=404,
                            detail=f'Question with id {question_id} does not exist')

    for choice in question.choices:
        if choice.id == question_vote.choice_id:
            choice.votes += 1
            return question

    raise HTTPException(status_code=404,
                        detail=f'Question {question_id} does not have choice '
                               f'with id {question_vote.choice_id}')
