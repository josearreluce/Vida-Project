# Vida-Project

Clone and run pip install -r requirements.txt 

1. Set environment variable: EXPORT FLASK_APP=app
2. Start the dev server with: python -m flask run

**Clarity of submission location, etc [4 points]**

github repo: Vida-Project/tests

**Unit test cases for first iteration development [28 points in total]**

 Unit test framework [2 points]
 
 - pytest framework
 
 To run the tests, use the command: pytest [file_name]

implementation: coverage of important features (thoroughness) [12 points]
 
 We implement tests based on feature coverage:
 1. test_db.py: tests about the database, where we store health information for the user and symptoms and conditions information, we check that the correct information is stored in the format we want. Specifically, we break this down into two test cases: one to ensure that only the credentials that can connect to the database are the correct ones, and another to ensure that syntactically correct queries with real values are returning correct results.
 3. test_backend.py: tests about the backend, symptom condition diagnosis and user profile set up
 4. test_graph.py: tests about the graph used for the symptom condition diagnosis
 

implementation: lack of redundancy (concision) [6 points]

Reflection of design goals and planned implementation (from milestone 1 and 2) [4 points]
 We based our design on a MVP that will give users an easy to use interface. Our design priorities are
 1. UI is intuitive and accessible
 2. The symptom to condition generation process is as accurate as possible
 3. The user information is stored correctly. <br />
 We have the database set-up in an AWS instance, and the initial app infrasctructure running as a Flask application. We are currently setting up the graph and will connect the graph to user input of symptoms and diagnoses. In milestone 2 we want to connect the functionality and create an initial clickable prototype where the user can enter a symptom and receive a diagnosis. We will then work on refining the graph algorithm so that diagnoses are accurate. <br />
 
Our tests reflect the design decisions above. We write tests to cover the three main design points, to make sure that the basic functionality of our application (symptom diagnosis) is available to the user.

code is easy to read and understand [4 points]
