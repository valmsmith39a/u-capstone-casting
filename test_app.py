import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2Mjk4NTgwNDQsImV4cCI6MTYyOTk0NDQ0NCwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6InBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBwb3N0Om1vdmllcyBkZWxldGU6bW92aWVzICBnZXQ6bW92aWVzIGdldDphY3RvcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0Om1vdmllcyIsImRlbGV0ZTptb3ZpZXMgIiwiZ2V0Om1vdmllcyIsImdldDphY3RvcnMiXX0.CFo5a_5G8d5cyH05skS-rDjtp40GXBFsxFJToXE-chVowGFFBV-leCtGFfVqKc1rae3Awr6NKne2yaVkm_LzUrGLWTofycf7QyGBoaIrvdwGdae4TdCUfVDrfVCfgQJeBYt0qUxNMASinKoCrkiDnpJ6tmckPUtYgWXF3O7NaPqn6JuIXYLuufhhEkbDxRoXDQAD3JUJ1Q408mvfR1xD2meBqTVX_GCB_LlVLhrTbdEEnvS3b6QOTJBtnIT6jKK71Zy4p8-pqWZtAFfFUmhbvO-bpbudI_YFk6f1mmjOoQVmPXxr80vFrlykYY_i8PKfxU1qMQVB2wU7IOQ2ONgVfg")


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
                                 headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_movies"])

    def test_create_actor(self):
        res = self.client().post("/actors/create",
                                 headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_actors"])

    def test_delete_movie(self):
        res = self.client().delete("/movies/2",
                                   headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_movies"])

    def test_delete_actor(self):
        res = self.client().delete("/actors/2",
                                   headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_actors"])

    def test_patch_movie(self):
        res = self.client().patch("/movies/2", json={"title": "patched title", "release_date": "1/1/2022"},
                                  headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_patch_actor(self):
        res = self.client().patch("/actors/1", json={"name": "patched name"},
                                  headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

        # Make tests executable
if __name__ == "__main__":
    unittest.main()
