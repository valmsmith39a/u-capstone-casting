# Udacity Capstone Project: Casting Agency

### Motivation

Final project for Udacity full stack nanodegree (backend focused) to implement multiple API endpoints for a casting agency to create, read, update, delete movies and actors. The endpoints are protected with an authentication token supporting role-based access control (RBAC). For example Casting Assistants can only get movies and actor names, but the Executive Producer can perform all actions including adding and deleting movies. Application is deployed at: `https://u-capstone-casting.herokuapp.com`

### Project Setup

Clone repository:  
`git clone https://github.com/valmsmith39a/u-capstone-casting.git`

Set up virtual environment:  
`python3 -m venv /path/to/new/virtual/environment`

Activate virtual environment:  
`. venv/bin/activate`

Install dependencies:  
`pip3 install -r requirements.txt`

Key Depedencies

- Flask: a micro web application framework
- SQLAlchemy: Python SQL toolkit and Object Relational Mapper

Environment variables:

```
export FLASK_APP=app.py
export FLASK_ENV=development
```

Run application:
`flask run or python3 app.py`

Export bearer token for Casting Assistant:

```
export BEARER_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MzAwMzQ3NDQsImV4cCI6MTYzMDYzOTU0NCwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6ImdldDptb3ZpZXMgZ2V0OmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDptb3ZpZXMiLCJnZXQ6YWN0b3JzIl19.x_Gq79JANKbggWPA5-8GnT8OzuNNIvDOzssygGcfGf291vCz6iOM0WdWoRq3PnWY0JbPhD-FIf3uCHyKBHmmeV8Cpsdq_NjKr9UsRFE89Rd1DVWGX5qMVc1fLWEjYVm9pBG9-1va6Q05Bhc6FfXJF0z94-iotay-cUIATN-2O1HsnrTkN2vmR4xYIcT_bym6x2-V1Ms7x7snLxja2XgqQb-NzEENo484EISh7tUMrIoOKOno65KanbOtfOy5L5VPTiz0SpUfiKeNaaq6n4B5-PtIISoCYty_iewzUrURssXqIN1zcRb10mI8L_lUYXFlUTxGcrf32xQtaWuwYdSmiA
```

Sample curl request:

```
curl http://localhost:5000/movies -H "Accept: application/json" -H "Authorization: Bearer $BEARER_TOKEN"
```

Response:

```
{
  "movies": [
    {
      "id": 9,
      "release_date": "1/1/2077",
      "title": "CyberMooMoo"
    },
    {
      "id": 5,
      "release_date": "2/2/2077",
      "title": "CyberCheese"
    },
    {
      "id": 6,
      "release_date": "3/3/2077",
      "title": "CyberLlama"
    }
  ],
  "success": true,
  "total_movies": 3
}

```

##### To run unit tests:

`python3 test_app.py`

### API Documentation

The API enables users to create, read, update and delete movies and actors based on the user's role.

Base URL: `https://u-capstone-casting.herokuapp.com/movies`

#### Roles

Casting Assistant:

- GET movies and actors
- BEARER_TOKEN:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MzAwMzQ3NDQsImV4cCI6MTYzMDYzOTU0NCwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6ImdldDptb3ZpZXMgZ2V0OmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDptb3ZpZXMiLCJnZXQ6YWN0b3JzIl19.x_Gq79JANKbggWPA5-8GnT8OzuNNIvDOzssygGcfGf291vCz6iOM0WdWoRq3PnWY0JbPhD-FIf3uCHyKBHmmeV8Cpsdq_NjKr9UsRFE89Rd1DVWGX5qMVc1fLWEjYVm9pBG9-1va6Q05Bhc6FfXJF0z94-iotay-cUIATN-2O1HsnrTkN2vmR4xYIcT_bym6x2-V1Ms7x7snLxja2XgqQb-NzEENo484EISh7tUMrIoOKOno65KanbOtfOy5L5VPTiz0SpUfiKeNaaq6n4B5-PtIISoCYty_iewzUrURssXqIN1zcRb10mI8L_lUYXFlUTxGcrf32xQtaWuwYdSmiA
```

Casting Director:

- Permissions of Casting Assistant
- Add (POST)/ Remove (DELETE) actors
- Modify (PATCH) movies and actors data
- BEARER_TOKEN:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MzAwMzc5MjksImV4cCI6MTYzMDY0MjcyOSwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6InBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBnZXQ6bW92aWVzIGdldDphY3RvcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJnZXQ6bW92aWVzIiwiZ2V0OmFjdG9ycyJdfQ.11bfa2BYw6CHxOapHcom8qs_1diKHj2KlzMhY1ALEkUCii0va-FkP8BdOWlgoIQPO_SMREb85Vs8dKG6XD_64XFac_WdrMDaqx6Y7A-5CnlAYCs-SiuVJ2nxVkUeIAAbpEQH_fChnGGv4MY53daQRcSIUvGJu5g8-lBjX5uLq8U3q3f58jkjFMDW5mhoFWbF5lqlzqHWR9uzatQIX9dzhc2sxA1sSk-zGhz2b2KjzwKU1FItD4KRDz2oK6MMhwv5QrEgGLIEKQKIZ9n5-NxknNgD7ToGK2taCqFTx-lB6Q94cx6Zmn-rTs5L2FnXKhczUyloO9zDZ78aGEvwroJa5Q
```

Executive Producer:

- Permissions of Casting Assistant and Casting Director
- Add (POST) / Remove (DELETE) movies
- BEARER_TOKEN:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVrMFJJZzRiWVpVVW1nZklURzZXOCJ9.eyJpc3MiOiJodHRwczovL2Rldi13YW9peDFwOS51cy5hdXRoMC5jb20vIiwic3ViIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1VAY2xpZW50cyIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MzAxMjEwNTAsImV4cCI6MTYzMDcyNTg1MCwiYXpwIjoiODZtN3dqSWxGVGJvNGFPNUlCQzZ4WGltbndFSkJpb1UiLCJzY29wZSI6InBvc3Q6YWN0b3JzIGRlbGV0ZTphY3RvcnMgcGF0Y2g6YWN0b3JzIHBhdGNoOm1vdmllcyBwb3N0Om1vdmllcyBkZWxldGU6bW92aWVzICBnZXQ6bW92aWVzIGdldDphY3RvcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJwb3N0OmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0Om1vdmllcyIsImRlbGV0ZTptb3ZpZXMgIiwiZ2V0Om1vdmllcyIsImdldDphY3RvcnMiXX0.SSnElDt5sgM2uM-2Eq7JBOXWRS9Usp0djZurejnzGwu0c-v7d-CfZ9hN3nyQsigiVY5kq5IicEoWgK1d4kTIHymqGAA-1A9pbXGkvtCEUdhYv5HvV_p8S3qedia2B_uzphMWjjVJXs-kngPAa7QBk4PjEIJz9RSX6NklI632_C4xvW3bIGLueOUf5VBLt_JFAcnxOyeqIJv5zJN1j4yig17pcGanBf8K72bs-XcFtNLIrXphYpf0-g6k9o7-FaeaiTMq09XG-8t_Tb0016Zj9IOZX-YE4Oj0qQDyMQZwg3UDTmQLec-exFYLOAyaE8VI4K8bWiXhP4ekkbPReCXjhQ
```

##### Example API Calls

Export a BEARER_TOKEN  
Example: `export BEARER_TOKEN=eyHhG...`

GET movies

```
curl https://u-capstone-casting.herokuapp.com/movies -H "Accept: application/json" -H "Authorization: Bearer $BEARER_TOKEN"
```

Response:

```
{"movies":[{"id":1,"release_date":"1/1/2077","title":"CyberCheese"},{"id":2,"release_date":"2/2/2077","title":"CyberMooMoo"},{"id":3,"release_date":"3/3/2077","title":"CyberLlama"}],"success":true,"total_movies":3}
```

GET ACTORS

```
curl https://u-capstone-casting.herokuapp.com/actors -H "Accept: application/json" -H "Authorization: Bearer $BEARER_TOKEN"
```

Response:

```
{"actors":[{"age":"29","gender":"M","id":5,"name":"John Cheese"},{"age":"28","gender":"F","id":6,"name":"Jane MooMoo"},{"age":"30","gender":"M","id":7,"name":"Larry Llama"}],"success":true,"total_actors":3}
```

POST movies

```
curl -d '{"title":"CyberCheese", "release_date":"1/1/2077"}' -H "Content-Type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -X POST https://u-capstone-casting.herokuapp.com/movies/create
```

Response:

```
{"created":{"id":73,"release_date":"1/1/2077","title":"CyberCheese"},"success":true,"total_movies":67}
```

POST actors

```
curl -d '{"name":"John Cheese", "age":"335", "gender":"M"}' -H "Content-Type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -X POST https://u-capstone-casting.herokuapp.com/actors/create
```

Response:

```
{"created":{"age":"335","gender":"M","id":57,"name":"John Cheese"},"success":true,"total_actors":52}
```

PATCH movies

```
curl -d '{"title":"CyberMooMooooo", "release_date":"3/3/3077"}' -H "Content-Type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -X PATCH https://u-capstone-casting.herokuapp.com/movies/70
```

Response:

```
{"movie":{"id":70,"release_date":"3/3/3077","title":"CyberMooMooooo"},"success":true}
```

PATCH actors

```
curl -d '{"name":"John MooMoo", "age":"335", "gender":"M"}' -H "Content-Type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -X PATCH https://u-capstone-casting.herokuapp.com/actors/9
```

Response:

```
{"actor":{"age":"335","gender":"M","id":9,"name":"John MooMoo"},"success":true}
```

DELETE movies

```
curl -H "Content-Type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -X DELETE https://u-capstone-casting.herokuapp.com/movies/70
```

Response:

```
{"deleted":70,"success":true,"total_movies":67}
```

DELETE actors

```
curl -H "Content-Type: application/json" -H "Authorization: Bearer $BEARER_TOKEN" -X DELETE https://u-capstone-casting.herokuapp.com/actors/38
```

Response:

```
{"deleted":38,"success":true,"total_actors":51}
```
