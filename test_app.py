import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MzAwMzQ3NDQsImV4cCI6MTYzMDYzOTU0NCwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6ImdldDptb3ZpZXMgZ2V0OmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDptb3ZpZXMiLCJnZXQ6YWN0b3JzIl19.x_Gq79JANKbggWPA5-8GnT8OzuNNIvDOzssygGcfGf291vCz6iOM0WdWoRq3PnWY0JbPhD-FIf3uCHyKBHmmeV8Cpsdq_NjKr9UsRFE89Rd1DVWGX5qMVc1fLWEjYVm9pBG9-1va6Q05Bhc6FfXJF0z94-iotay-cUIATN-2O1HsnrTkN2vmR4xYIcT_bym6x2-V1Ms7x7snLxja2XgqQb-NzEENo484EISh7tUMrIoOKOno65KanbOtfOy5L5VPTiz0SpUfiKeNaaq6n4B5-PtIISoCYty_iewzUrURssXqIN1zcRb10mI8L_lUYXFlUTxGcrf32xQtaWuwYdSmiA")
CASTING_DIRECTOR = ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MzAwMzc5MjksImV4cCI6MTYzMDY0MjcyOSwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6InBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBnZXQ6bW92aWVzIGdldDphY3RvcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJnZXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyJdfQ.11bfa2BYw6CHxOapHcom8qs_1diKHj2KlzMhY1ALEkUCii0va-FkP8BdOWlgoIQPO_SMREb85Vs8dKG6XD_64XFac_WdrMDaqx6Y7A-5CnlAYCs-SiuVJ2nxVkUeIAAbpEQH_fChnGGv4MY53daQRcSIUvGJu5g8-lBjX5uLq8U3q3f58jkjFMDW5mhoFWbF5lqlzqHWR9uzatQIX9dzhc2sxA1sSk-zGhz2b2KjzwKU1FItD4KRDz2oK6MMhwv5QrEgGLIEKQKIZ9n5-NxknNgD7ToGK2taCqFTx-lB6Q94cx6Zmn-rTs5L2FnXKhczUyloO9zDZ78aGEvwroJa5Q")
EXECUTIVE_PRODUCER = ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MzAwMzM5MjksImV4cCI6MTYzMDEyMDMyOSwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6InBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBwb3N0Om1vdmllcyBkZWxldGU6bW92aWVzICBnZXQ6bW92aWVzIGdldDphY3RvcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0Om1vdmllcyIsImRlbGV0ZTptb3ZpZXMgIiwiZ2V0Om1vdmllcyIsImdldDphY3RvcnMiXX0.xmd5fXkmp8XiQzNGNsV0i4uSucf2Mn0DzSj2vUhagt9LHUenxApW85ByD37DF_TtYHPngBVv00pPkYO6GsRhP96Q5sAmpOP803wpNa9v54nzC614os5XsJXENnSCsAmWflkL-oW9D_NHfr0Ux2f9XB7CByxg0WnR08wX4xsKItob4VEtn6nXAofJYflW9-roaKjjOYYTCzlFX8v-m1PB2GWwL08OgDUb_LvKZ6a-OyefCp3FrXwgEDoTvTVLx6-WmBLuAh0N44LUGS3d0ZZFXOA4pyyiFjveH9c3zXdMLTZXaLp4vHOT-lokdifSqivrYHSfgIp0O0QUQQbNPfuoQA")


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
    # test RBAC CASTING ASSISTANT success case

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

    # test RBAC CASTING ASSISTANT failure case
    def test_rbac_failure_casting_assistant(self):
        res = self.client().post("/movies/create",
                                 headers={
                                     "Authorization": f'Bearer {CASTING_ASSISTANT}'},
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "unauthorized")
        self.assertEqual(data["description"],
                         "User permission not found in permissions")

    # test RBAC EXECUTIVE PRODUCER
    def test_create_movie(self):
        res = self.client().post("/movies/create",
                                 headers={
                                     "Authorization": f'Bearer {EXECUTIVE_PRODUCER}'},
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_movies"])

    def test_create_actor(self):
        res = self.client().post("/actors/create",
                                 headers={
                                     "Authorization": f'Bearer {CASTING_DIRECTOR}'},
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_actors"])

    # Note to reviewer: Test case may fail if movie with id 1 not created yet
    def test_delete_movie(self):
        res = self.client().delete("/movies/1",
                                   headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_movies"])

    # Note to reviewer: Test case may fail if movie with id 1 not created yet
    def test_delete_actor(self):
        res = self.client().delete("/actors/1",
                                   headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_actors"])

    # test CASTING DIRECTOR success case
    def test_patch_movie(self):
        res = self.client().patch("/movies/1", json={"title": "patched title", "release_date": "1/1/2022"},
                                  headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_patch_actor(self):
        res = self.client().patch("/actors/1", json={"name": "patched name"},
                                  headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    # test RBAC CASTING DIRECTOR failure case
    def test_rbac_failure_casting_director(self):
        res = self.client().post("/movies/create",
                                 headers={
                                     "Authorization": f'Bearer {CASTING_DIRECTOR}'},
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "unauthorized")
        self.assertEqual(data["description"],
                         "User permission not found in permissions")

    def test_404_if_movie_does_not_exist(self):
        res = self.client().get("movies/no-resource-here")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_422_unprocessable(self):
        res = self.client().post("/movies/create",
                                 headers={
                                     "Authorization": f'Bearer {EXECUTIVE_PRODUCER}'},
                                 content_type='multipart/form-data',
                                 data=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


        # Make tests executable
if __name__ == "__main__":
    unittest.main()
