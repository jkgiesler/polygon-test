from flask import Flask, request, jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modified_models import User, Question, Option, Attempt
app = Flask(__name__)

Base = declarative_base()

engine = create_engine('sqlite:///bookquestions.db', echo=True)
#Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user_one = User(email = 'jason.giesler@gmail.com')
user_one.hash_password('thisissecure')

user_two = User(email = 'bobloblaw@bobloblawlawblog.com')
user_two.hash_password('mouthfull')

question_one = Question(book_id="Bob Loblaw's Law Blog",create_by = 2,explanation = "How do I file for divorce?",likes = 30,dislikes = 10)
q1_option1 = Option(question_id = 1,content = "talk to a lawyer",correct = True)
q1_option2 = Option(question_id = 1, content = "talk to a pastor",correct = False)

question_two = Question(book_id="Bob Loblaw's Law Blog",create_by = 2,explanation = "How do I file a restraining order",likes = 5,dislikes = 50)
q2_option1 = Option(question_id = 2,content = "file a police report",correct = True)
q2_option2 = Option(question_id = 2,content = "buy a handgun",correct = False)

q1_attempt1 = Attempt(question_id = 1,user_id = 1, guessed = 1, correct = False)
q1_attempt2 = Attempt(question_id = 1,user_id = 1, guessed = 1, correct = False)
q1_attempt3 = Attempt(question_id = 1,user_id = 1, guessed = 2, correct = True)

q2_attempt1 = Attempt(question_id = 2,user_id = 1, guessed = 4, correct = False)
q2_attempt2 = Attempt(question_id = 2,user_id = 1, guessed = 3, correct = True)




session.add_all([user_one,user_two,question_one,question_two,
	q1_option1,q1_option2,q2_option1,q2_option2,q1_attempt1,q1_attempt2,q1_attempt3,
	q2_attempt1,q2_attempt2])

session.commit()


