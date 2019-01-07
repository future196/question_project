
from ext import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(64), nullable=False)

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get("telephone")
        username = kwargs.get("username")
        password = kwargs.get("password")
        icon = kwargs.get("icon")

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)
        self.icon = icon

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result




class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref=db.backref('questions'))


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(30), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    answer_time = db.Column(db.DateTime, default=datetime.now)
    author = db.relationship("User", backref=db.backref('answers'))
    question = db.relationship("Question", backref=db.backref('answers'))