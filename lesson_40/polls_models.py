from pydantic import BaseModel
from typing import List


class Choice(BaseModel):
    id: int
    choice_text: str
    votes: int
    question: int


class Question(BaseModel):
    id: int
    question_text: str
    pub_date: str
    status: str
    choices: List[Choice]


class BasePagination(BaseModel):
    count: int
    next: str | None = None
    previous: str | None = None

    # field `results` must be added in a subclass


class PaginatedQuestions(BasePagination):
    results: list[Question]


class Database:
    def __init__(self):
        self._questions = self._generate_fake_questions()

    def _generate_fake_questions(self):
        fake_questions = [
            Question(
                id=1,
                question_text="What is your favorite color?",
                pub_date="2024-03-01",
                status="active",
                choices=[
                    Choice(id=1, choice_text="Red", votes=0, question=1),
                    Choice(id=2, choice_text="Blue", votes=0, question=1),
                    Choice(id=3, choice_text="Green", votes=0, question=1),
                ]
            ),
            Question(
                id=2,
                question_text="What is your favorite animal?",
                pub_date="2024-03-01",
                status="active",
                choices=[
                    Choice(id=4, choice_text="Dog", votes=0, question=2),
                    Choice(id=5, choice_text="Cat", votes=0, question=2),
                    Choice(id=6, choice_text="Bird", votes=0, question=2),
                ]
            ),
            Question(
                id=3,
                question_text="What is your favorite food?",
                pub_date="2024-03-01",
                status="active",
                choices=[
                    Choice(id=7, choice_text="Pizza", votes=0, question=3),
                    Choice(id=8, choice_text="Sushi", votes=0, question=3),
                    Choice(id=9, choice_text="Burger", votes=0, question=3),
                ]
            ),
            Question(
                id=4,
                question_text="What is your favorite programming language?",
                pub_date="2024-03-01",
                status="active",
                choices=[
                    Choice(id=10, choice_text="Python", votes=0, question=4),
                    Choice(id=11, choice_text="Java", votes=0, question=4),
                    Choice(id=12, choice_text="JavaScript", votes=0, question=4),
                ]
            ),
            Question(
                id=5,
                question_text="What is your favorite season?",
                pub_date="2024-03-01",
                status="active",
                choices=[
                    Choice(id=13, choice_text="Spring", votes=0, question=5),
                    Choice(id=14, choice_text="Summer", votes=0, question=5),
                    Choice(id=15, choice_text="Autumn", votes=0, question=5),
                    Choice(id=16, choice_text="Winter", votes=0, question=5),
                ]
            ),
        ]
        return fake_questions

    def get_questions(self) -> list[Question]:
        return self._questions

    def get_question(self, question_id: int) -> Question | None:
        for q in self._questions:
            if q.id == question_id:
                return q
        return None


# Пример использования
if __name__ == "__main__":
    db = Database()
    for question in db.questions:
        print(question.dict())
