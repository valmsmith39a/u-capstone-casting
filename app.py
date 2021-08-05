import os
from flask import Flask
from models import setup_db, Movie, Actor
from flask_cors import CORS


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route('/movies/create')
    def create_movie():
        new_movie = Movie(title='Cyberpunkerdoodle', release_date='1/1/2077')
        new_movie.insert()
        movies = Movie.query.all()
        print('movies', movies)
        return 'movie created'
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
