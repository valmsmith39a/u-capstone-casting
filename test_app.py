import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2Mjk5NTExNjMsImV4cCI6MTYzMDAzNzU2MywiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6InBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBwb3N0Om1vdmllcyBkZWxldGU6bW92aWVzICBnZXQ6bW92aWVzIGdldDphY3RvcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0Om1vdmllcyIsImRlbGV0ZTptb3ZpZXMgIiwiZ2V0Om1vdmllcyIsImdldDphY3RvcnMiXX0.qaRtgxbduLroGRm8QcyfBFGZi8sc4CgFbIwci-JI2-ylAr2WmPbSs2OlNfLtgy7eRRLtvqQnsH837fG4avxKRsI7_3qPzcLaHSwMRGlJ-taZfVDEUprDZzlbPOu_9fJhMcSYPKI4REqJuVhA5bNygZ7zpF3roWZKa7AucLIuYUwx8Cx5goIp63AHyQVZGIw_7-VqFgHfjLKa__89MQUWAN10LmoKL4oHWA4TT6uPeaVNqJ0dtVNlTeKyIvjMYhqYQlTqtc60cXqhU0pwgmYSD4H5gF9Z_-m_74d46dYmzMbN6FpD5YP0Wr5W7Hs6COaYhNw_ZEBp6ICAqBdCvagODg")


class CastingTestCase(unittest.TestCase):
    """This class represents Casting test cases"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "d9ph6ud07tsfsv"
        self.database_path = os.getenv("DATABASE_URL")
        setup_db(self.app, self.database_path)

        self.new_movie = {
            "title": "Dinosaur Movie",
            "release_date": "1/1/2022"
        }

        self.new_actor = {
            "name": "John Wick",
            "age": "49",
            "gender": "M",
            "movie_id": 1
        }

        # bind app to current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    """
	Tests
	"""

    def test_get_movies(self):
        res = self.client().get(
            "/movies", headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))
        self.assertTrue(data["total_movies"])

    def test_get_actors(self):
        res = self.client().get(
            "/actors", headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))
        self.assertTrue(data["total_actors"])

    def test_create_movie(self):
        res = self.client().post("/movies/create",
                                 headers={
                                     "Authorization": f'Bearer {CASTING_ASSISTANT}'},
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_movies"])

    def test_create_actor(self):
        res = self.client().post("/actors/create",
                                 headers={
                                     "Authorization": f'Bearer {CASTING_ASSISTANT}'},
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_actors"])

    # def test_delete_movie(self):
    #     res = self.client().delete("/movies/2",
    #                                headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_movies"])

    # def test_delete_actor(self):
    #     res = self.client().delete("/actors/2",
    #                                headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["total_actors"])

    def test_patch_movie(self):
        res = self.client().patch("/movies/11", json={"title": "patched title", "release_date": "1/1/2022"},
                                  headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_patch_actor(self):
        res = self.client().patch("/actors/12", json={"name": "patched name"},
                                  headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_404_if_movie_does_not_exist(self):
        res = self.client().get("movies/no-resource-here")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_422_unprocessable(self):
        res = self.client().post("/movies/create",
                                 headers={
                                     "Authorization": f'Bearer {CASTING_ASSISTANT}'},
                                 content_type='multipart/form-data',
                                 data=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

        # Make tests executable
if __name__ == "__main__":
    unittest.main()
