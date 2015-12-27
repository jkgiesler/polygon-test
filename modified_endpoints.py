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

@app.route("/user/<userid>")
def user(userid):
	return getUser(userid)

@app.route("/questions/<bookid>")
def book_questions(bookid):
	return getBookQuestions(bookid)

@app.route("/options/<questionid>")
def question_options(questionid):
	return getQuestionOptions(questionid)

'''
@app.route("/testpush")
def push_data():


	data = Question(123,342,'This is a test',12,1)
	session.add(data)
	session.commit()
	query = session.query(Question)
	return jsonify(Question = [i.serialize for i in query])
'''

def getUser(userid):
	user = session.query(User).filter(User.id == userid)
	return jsonify(User=[i.serialize for i in user])

def getBookQuestions(bookid):
	questions = session.query(Question).filter(Question.book_id == bookid)
	return jsonify(Question=[i.serialize for i in questions])

def getQuestionOptions(questionid):
	options = session.query(Option).filter(Option.question_id == questionid)
	return jsonify(Option=[i.serialize for i in options])

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5555)