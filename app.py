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
        return jsonify({
            "success": True,
            "created": new_actor.format(),
            "total_actors": len(actors)
        })
        
    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):
        try:
            movie = Movie.query.filter(movie_id == Movie.id).one_or_none()
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
            
    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    def delete_actor(actor_id):
        try:
            actor = Actor.query.filter(actor_id == Actor.id).one_or_none()
            actor.delete()
            actors = format(Actor.query.order_by(Actor.id).all())
            return jsonify({
                "success": True,
                "deleted": actor_id,
                "actors": actors,
                "total_actors": len(actors)
            })

        except:
            abort(422)

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    def update_movie(movie_id):
        try:
            if movie_id is None:
                abort(404)
            
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            new_movie_data = request.get_json()

            if "title" in new_movie_data:
                new_title = new_movie_data["title"]
                movie.title = new_title

            if "release_date" in new_movie_data:
                new_release_date = new_movie_data["release_date"]
                movie.release_date = new_release_date

            movie.update()
            
            return jsonify({"success": True, "movie": movie.format()})
        
        except:
            abort(422)
   
    return app


app=create_app()

if __name__ == '__main__':
    app.run()
