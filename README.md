# Udacity Capstone Project: Casting Agency

### Motivation

Final project for Udacity full stack nanodegree (backend focused) to implement multiple API endpoints for a casting agency to create, read, update, delete movies and actors. The endpoints are protected with an authentication token supporting role-based access control (RBAC). For example Casting Assistants can only get movies and actor names, but the Executive Producer can perform all actions including adding and deleting movies.

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
