from sqlalchemy import Column, Integer, String, Enum, Float, Text, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	date_joined = Column(DateTime, default=func.now())
	email = Column(String(32), index=True)
	password_hash = Column(String(64))
	created_questions = relationship('Question')
	question_attempts = relationship('Attempt')

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	@property
	def serialize(self):
	    return {
	    	'id': self.id,
	    	'date_joined': self.date_joined,
	    	'email': self.email,
	    	'password': self.password_hash,
	    	#created questions needs to be a string not a dict
	    	'created_questions': "|".join([str(i.serialize['id'])+" "+i.serialize['book_id'] for i in self.created_questions]),
	    	'question_attempts': "|".join([str(i.serialize['question_id']) + " "+str(i.serialize['id']) + " "+str(i.serialize['correct']) for i in self.question_attempts])
	    }

class Attempt(Base):
	__tablename__ = 'attempt'
	id = Column(Integer, primary_key=True)
	date_attempted = Column(DateTime, default=func.now())
	guessed = Column(Integer, ForeignKey('option.id'))
	question_id = Column(Integer, ForeignKey('question.id'))
	user_id = Column(Integer, ForeignKey('user.id'))
	correct = Column(Boolean)

	@property
	def serialize(self):
	    return {
	    	'id': self.id,
	    	'date_attempted': self.date_attempted,
	    	'question_id': self.question_id,
	    	'user_id': self.user_id,
	    	'correct': self.correct
	    }
		
#Every book will have questions. These will be multiple choice and might have more than four options.
class Question(Base):
	__tablename__ = 'question'
	id = Column(Integer, primary_key=True)
	book_id = Column(String(30)) #This will talk to the google books api and we can get the cover art and stuff.
	create_by = Column(Integer, ForeignKey('user.id'))
	date_modified = Column(DateTime, default=func.now()) #Do we need to keep track of modified AND created?
	options = relationship('Option')
	attempts = relationship('Attempt')
	explanation = Column(String(1000)) #We might want to make this a separate table and include an optional picture link
	likes = Column(Integer)
	dislikes = Column(Integer)

	@property
	def serialize(self):
	    return {
	    	'id': self.id,
	    	'book_id': self.book_id,
	    	'create_by': self.create_by,
	    	'options': "\t".join([str(i.serialize['id']) for i in self.options]), # how is this really supposed to be?
	    	'date_modified': self.date_modified,
	    	'explanation': self.explanation,
	    	'likes': self.likes,
	    	'dislikes': self.dislikes
	    }
	

#Every option is related to a question and should be able to be edited or removed from that question.
class Option(Base):
	__tablename__ = 'option'
	id = Column(Integer, primary_key=True)
	date_modified = Column(DateTime, default=func.now()) #Do we need to keep track of modified AND created?
	question_id = Column(Integer, ForeignKey('question.id'))
	correct = Column(Boolean)
	content = Column(String(1000)) #We might want an optional picture link later.

	@property
	def serialize(self):
	    return {
	    	'id': self.id,
	    	'date_modified': self.date_modified,
	    	'question_id': self.question_id,
	    	'content': self.content
	    }
engine = create_engine('sqlite:///bookquestions.db', echo=True)
Base.metadata.create_all(engine)