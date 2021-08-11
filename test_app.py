import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = ("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2Mjg2NDUxNDUsImV4cCI6MTYyODczMTU0NSwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6InBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBwb3N0Om1vdmllcyBkZWxldGU6bW92aWVzICBnZXQ6bW92aWVzIGdldDphY3RvcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0Om1vdmllcyIsImRlbGV0ZTptb3ZpZXMgIiwiZ2V0Om1vdmllcyIsImdldDphY3RvcnMiXX0.oogXltKO-8OWezCE4DjjMsRiKuY1rqfue4pnINMBVNv1QJ1mKdyVEodG60_0AuTCf7429UdLV7Xx0aQFnPC4Qc2qKgIzochjMd_tdViyB9FZiepzINe6g91vJatqq7ZQ5TJoLeTS23IerpyCFWOVT_fhwyuIJ7MEpVaImJj5uDJNSGRNIhk668UK1-hBNUBVYZxoqrztk_33KVUykXOpUbK4De_QPvsPr_Auw5KystjsGzN9cbuXXYBqFeRLvhOuO2G4g6k7omq0YnWtDH2XU__fR6rLNYC_qkmEhH3HraciM0mwNKEasaVGImSnyfl_57COCI3ZxTKMWx0xXrglCw")


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


# Make tests executable
if __name__ == "__main__":
    unittest.main()
