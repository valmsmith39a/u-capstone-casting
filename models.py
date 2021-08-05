from typing import AsyncGenerator
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer
import json
import os

database_path = os.getenv("DATABASE_URL")

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movie
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    release_date = db.Column(db.String(120))

    def __repr__(self):
        return f'Movie: id({self.id}), title({self.title})'

    def insert(self):
        db.session.add(self)
        db.session.commit()


'''
Actor
'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))

    def __repr__(self):
        return f'Actor: id({self.id}), name({self.name})'


'''
Person
Have title and release year
'''


class Person(db.Model):
    __tablename__ = 'People'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    catchphrase = Column(String)

    def __init__(self, name, catchphrase=""):
        self.name = name
        self.catchphrase = catchphrase

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'catchphrase': self.catchphrase}
