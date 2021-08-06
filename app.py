import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movie, Actor
from flask_cors import CORS
from utils import format


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route("/")
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        return greeting

    @app.route("/coolkids")
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route("/movies")
    def get_movies():
        movies = format(Movie.query.all())
        return jsonify({
            "success": True,
            "movies": movies,
            "total_movies": len(movies)
        })

    @app.route("/actors")
    def get_actors():
        actors = format(Actor.query.all())
        return jsonify({
            "success": True,
            "actors": actors,
            "total_actors": len(actors)
        })

    @app.route("/movies/create", methods=["POST"])
    def create_movie():
        new_movie = Movie(title='Cyberpunkerdoodle', release_date='1/1/2077')
        new_movie.insert()
        movies = format(Movie.query.all())
        print('movies', movies)
        return jsonify({
            "success": True,
            "created": new_movie.format(), 
            "movies": movies,
            "total_movies": len(movies)
        })


    @app.route("/actors/create", methods=["POST"])
    def create_actor():
        new_actor = Actor(name="funnie man", gender="M", age="29")
        new_actor.insert()
        actors = Actor.query.all()
        print('actors', actors)
        return jsonify({
            "success": True,
            "created": new_actor.format(),
            "total_actors": len(actors)
        })
    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        try:
            movie = Movie.query.filter(movie_id == Movie.id).one_or_none()
            print('movie is', movie)
            movie.delete()
            movies = format(Movie.query.order_by(Movie.id).all())
            return jsonify({
                "success": True,
                "deleted": movie_id,
                "movies": movies,
                "total_movies": len(movies)
            })
        except:
            abort(422) 
            
            
    return app


app=create_app()

if __name__ == '__main__':
    app.run()
