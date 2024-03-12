from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os


Base = declarative_base()


class Question(Base):
   __tablename__ = 'question'
   id = Column(Integer, primary_key=True, autoincrement=True)
   question_text = Column(String(300))

   choices = relationship('Choice', back_populates='question')


class Choice(Base):
    __tablename__ = 'choice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    choice_text = Column(String(300))
    votes = Column(Integer, default=0)

    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship('Question', back_populates='choices', uselist=False)


DB_PATH = os.path.abspath('db.sqlite')


def create_database_session():
    engine = create_engine(f'sqlite:////{DB_PATH}', echo=False)
    if not database_exists(engine.url):
        create_database(engine.url)

    Session = sessionmaker(engine)
    return Session()
