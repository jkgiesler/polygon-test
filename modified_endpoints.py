from flask import Flask, request, jsonify
import json
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

@app.route("/questions/<bookid>",methods = ['GET','POST'])
def book_questions(bookid):
	if request.method == 'GET':
		return getBookQuestions(bookid)
	elif request.method == 'POST':
		#Question(book_id="Bob Loblaw's Law Blog",,create_by = 2,explanation = "How do I file for divorce?",likes = 30,dislikes = 10)
		data = request.form
		print(data)
		book_val = data['name']
		explanation_val = data['question']
		print(book_val)
		print(explanation_val)
		to_input = Question(book_id = book_val,create_by = 2,explanation = explanation_val,likes = 1,dislikes = 0)
		session.add(to_input)
		session.commit()
		return "success"


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
	data = [i.serialize for i in user]
	#return jsonify(User=[i.serialize for i in user])
	return json.dumps(data)

def getBookQuestions(bookid):
	questions = session.query(Question).filter(Question.book_id == bookid)
	data = [i.serialize for i in questions]
	return json.dumps(data)

def getQuestionOptions(questionid):
	options = session.query(Option).filter(Option.question_id == questionid)
	data = [i.serialize for i in options]
	#return jsonify(Option=[i.serialize for i in options])
	return json.dumps(data)
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5555)