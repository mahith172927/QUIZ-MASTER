from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)  
    full_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    
    scores=db.relationship("Scores",backref="player",lazy=True,cascade="all,delete")

class Subject(db.Model):
    __tablename__="subject"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    description=db.Column(db.String(100),nullable=True)

class Chapter(db.Model):
    __tablename__="chapter"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    description=db.Column(db.String(100),nullable=True)
    subject_id=db.Column(db.Integer,db.ForeignKey('subject.id',ondelete="CASCADE"),nullable=False)
    subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True))
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True,cascade="all ,delete")
    
class Quiz(db.Model):
    __tablename__="quiz"
    id=db.Column(db.Integer,primary_key=True)
    chapter_id=db.Column(db.Integer,db.ForeignKey('chapter.id',ondelete="CASCADE"),nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Time, nullable=False)  
    remarks = db.Column(db.String(200), nullable=True)  

    scores = db.relationship('Scores', backref='quiz', lazy=True,cascade="all,delete")
    questions=db.relationship('Questions',backref='quiz',lazy=True,cascade="all,delete")

class Questions(db.Model):
    __tablename__="questions"
    id=db.Column(db.Integer,primary_key=True) 
    quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id',ondelete="CASCADE"),nullable=False)
    question_statement=db.Column(db.String(200),nullable=False)
    option1=db.Column(db.String(100),nullable=False)
    option2=db.Column(db.String(100),nullable=False)        
    option3=db.Column(db.String(100),nullable=False)
    option4=db.Column(db.String(100),nullable=False)
    correct_answer=db.Column(db.String(100),nullable=False)

    
class Scores(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id',ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime)
    total_scored = db.Column(db.Float, nullable=False)   
    
    
 

def create_tables(app):
    with app.app_context():
        db.create_all()
