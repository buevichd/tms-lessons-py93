from pydantic import BaseModel
from typing import List
from models import Choice, Question


class ChoiceData(BaseModel):
    id: int
    choice_text: str
    votes: int
    question: int


class QuestionData(BaseModel):
    id: int
    question_text: str
    pub_date: None | str = None
    status: None | str = None
    choices: List[ChoiceData]


class BasePaginationData(BaseModel):
    count: int
    next: str | None = None
    previous: str | None = None

    # field `results` must be added in a subclass


class PaginatedQuestionsData(BasePaginationData):
    results: list[QuestionData]


def serialize_choice(choice: Choice) -> ChoiceData:
    return ChoiceData(id=choice.id, choice_text=choice.choice_text, votes=choice.votes,
                      question=choice.question.id)


def serialize_question(question: Question) -> QuestionData:
    return QuestionData(id=question.id, question_text=question.question_text,
                        choices=[serialize_choice(choice) for choice in question.choices])
