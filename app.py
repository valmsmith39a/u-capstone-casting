import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Movie, Actor
from flask_cors import CORS
from utils import format

from auth import requires_auth, AuthError


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
    @requires_auth("get:movies")
    def get_movies(jwt):
        try:
            movies = format(Movie.query.all())
            return jsonify({
                "success": True,
                "movies": movies,
                "total_movies": len(movies)
            })
        except:
            abort(422)

    @app.route("/actors")
    @requires_auth("get:actors")
    def get_actors(jwt):
        try:
            actors = format(Actor.query.all())
            return jsonify({
                "success": True,
                "actors": actors,
                "total_actors": len(actors)
            })
        except:
            abort(422)

    @app.route("/movies/create", methods=["POST"])
    @requires_auth("post:movies")
    def create_movie(jwt):
        try:
            body = request.get_json()
            title = body.get("title", None)
            release_date = body.get("release_date", None)

            new_movie = Movie(title=title,
                              release_date=release_date)
            new_movie.insert()
            movies = format(Movie.query.all())
            return jsonify({
                "success": True,
                "created": new_movie.format(),
                "total_movies": len(movies)
            })
        except:
            abort(422)

    @app.route("/actors/create", methods=["POST"])
    @requires_auth("post:actors")
    def create_actor(jwt):
        try:
            body = request.get_json()
            name = body.get("name", None)
            gender = body.get("gender", None)
            age = body.get("age", None)

            new_actor = Actor(name=name, gender=gender, age=age)
            new_actor.insert()
            actors = Actor.query.all()
            return jsonify({
                "success": True,
                "created": new_actor.format(),
                "total_actors": len(actors)
            })
        except:
            abort(422)

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(movie_id == Movie.id).one_or_none()
            movie.delete()
            movies = format(Movie.query.order_by(Movie.id).all())
            return jsonify({
                "success": True,
                "deleted": movie_id,
                "total_movies": len(movies)
            })
        except:
            abort(422)

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(actor_id == Actor.id).one_or_none()
            actor.delete()
            actors = format(Actor.query.order_by(Actor.id).all())
            return jsonify({
                "success": True,
                "deleted": actor_id,
                "total_actors": len(actors)
            })

        except:
            abort(422)

    @app.route("/movies/<int:movie_id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def update_movie(jwt, movie_id):
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

    @app.route("/actors/<int:actor_id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def update_actor(jwt, actor_id):
        try:
            if actor_id is None:
                abort(404)

            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            new_actor_data = request.get_json()

            if "name" in new_actor_data:
                new_name = new_actor_data["name"]
                actor.name = new_name

            if "age" in new_actor_data:
                new_age = new_actor_data["age"]
                actor.age = new_age

            if "gender" in new_actor_data:
                new_gender = new_actor_data["gender"]
                actor.gender = new_gender

            actor.update()

            return jsonify({"success": True, "actor": actor.format()})

        except:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def not_processed(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        })

    @app.errorhandler(AuthError)
    def auth_error(res):
        error = jsonify(res.error)
        status_code = res.status_code
        return error, status_code

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
