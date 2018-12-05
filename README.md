# Vida-Project
# Authors: Jose Arreluce, Will Darling, Max Demers, Miles Grogger, Andy Ham, Bruno Jacob, Thomas Jacobs, Qi Jin
# Original repo: "https://github.com/josearreluce/Vida-Project.git"

---------------------------------------------------------------------------------------------------

# Preface

Due to rising healthcare costs and increased access to health condition information through the
internet, more people than ever are looking to the internet to diagnosis potential health problems.
However, the quality of these diagnoses is often too ambiguous or severe to be useful. Vida attempts
to solve the problem by providing a more in-depth consultation process, and in turn a more accurate
and reasonable diagnosis, than the current providers (e.g. Google Search and WebMD).

---------------------------------------------------------------------------------------------------

# Installation Guide

Simply run the following terminal commands

$ git clone https://github.com/josearreluce/Vida-Project.git
$ cd Vida-Project
$ pip3 install -r requirements.txt
$ python3 -m flask run

Then navigate to http://127.0.0.1:5000/ in your browser to access the web application.

NOTE: We have found the most success running our application in Firefox. Google Chrome has been
      particularly difficult.

---------------------------------------------------------------------------------------------------

# Usage Guide

We designed Vida to be intuitive to navigate and use. While a user profile isn't required to start
an assessment, it's highly recommended. Once an assessment begins, type your most prominent symptom
into the search bar and select the matching entry. This begins the inquiry process. Note that Vida
currently only supports 12 starting symptoms (a full list is found in the appendix). Answer the
subsequent questions, and at the end Vida will provide a diagnosis.

---------------------------------------------------------------------------------------------------

# Running the Unit Tests

First download a chrome webdriver from http://chromedriver.chromium.org/downloads
and place the driver into the test directory.

The UI Tests require downloading this webdriver.

Then from within the tests directory run:
$ pytest -p no:warnings

NOTE: For further information on running unit tests, refer to the appendix

---------------------------------------------------------------------------------------------------

# Poorly Handled Inputs

Vida currently has difficulty handling top level symptoms "Dilated Pupils" and "Diarrhea"

---------------------------------------------------------------------------------------------------

# Implementation Overview

In this final round of development we greatly improved the functionality around user profile
information. When adding information, a single error in one field will not erase all changes from
that session, and there are more stringent checks to prevent users from entering unrealistic data.
We also added password salting for improved security. Finally, the user's health information is
properly implemented in the assessment process. At the end of the questionaire, the probabilities
are filtered based on the user information before a final diagnosis is reached.

---------------------------------------------------------------------------------------------------

# Who did what

Bayesian graph logic: Alex, Andy, Bruno, Qi
Database: Alex, Miles, Will
Front end: Jose, Max, Will
User Functionality: Max, Qi

---------------------------------------------------------------------------------------------------

# Changes from the Design Document

We were not able to implement a user's assessment history, or add time-based variables to the
assessment process (i.e. how long have you had a cough?).

---------------------------------------------------------------------------------------------------

# Others


---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

                                          ### Appendix ###

---------------------------------------------------------------------------------------------------

# Supported Conditions

"apendicitis"
"bronchitis"
"common cold"
"gastroenteritis"
"hangover"
"hernia"
"indigestion"
"pregnant"
"rabies"
"sinusitis"
"strep throat"
"testicular torsion"

# Supported Top Level Sympotms (these are the only symptoms that begin an assessment)

"abdominal pain"
"indigestion"
"diarrhea"
"change in bowel habits"
"loss of appetite"
"nausea"
"fever"
"fatigue"
"itchiness"
"eye itchiness"
"vertigo"
"sore throat"
"irritability"
"thirst"
"mental confusion"
"loss of muscle function"
"missed period"
"light spotting"
"increased sensitivity"
"pus"
"blood in stool"
"dilated pupils"
"body ache"
"malaise"
"itchy nose"
"shortness of breath"
"bulging in groin"
"changes in urination"
"inflammation of ear"
"headache"
"pain in face"
"testicular pain"
"tenderness"
"cough"
"congestion"

---------------------------------------------------------------------------------------------------

## Archived notes from iteration 2:

#Suggested Acceptance Testing:

We've expanded the user functionality significantly, so try playing around with the new features.
Though we've now populated the database with real symptom and condition data to inform the diagnosis
process, we still had trouble pulling names from the database to the front end. So while the back
end diagnosis process is using real symptom/condition data, from the user-perspective the data is
generic.

# Implementation Overview

We refined our front end design, and expanded the back end. Firstly, users can now submit
background health information to help with their diagnosis, and their diagnosis history is stored
with their account. We also implemented proper user sessions, password hashing, and password
strength requirements. The database is now fully populated with real symptoms and conditions that
are used to build an updated version of Vida's Bayesian graph model, and users will see the symptoms and conditions when they start assessment.

The conditions supported are:
"apendicitis"
"bronchitis"
"common cold"
"gastroenteritis"
"hangover"
"hernia"
"indigestion"
"pregnant"
"rabies"
"sinusitis"
"strep throat"
"testicular torsion"

And the top level symptoms (which are used to start the diagnosis process) are:
"abdominal pain"
"indigestion"
"diarrhea"
"change in bowel habits"
"loss of appetite"
"nausea"
"fever"
"fatigue"
"itchiness"
"eye itchiness"
"vertigo"
"sore throat"
"irritability"
"thirst"
"mental confusion"
"loss of muscle function"
"missed period"
"light spotting"
"increased sensitivity"
"pus"
"blood in stool"
"dilated pupils"
"body ache"
"malaise"
"itchy nose"
"shortness of breath"
"bulging in groin"
"changes in urination"
"inflammation of ear"
"headache"
"pain in face"
"testicular pain"
"tenderness"
"cough"
"congestion"

# Who did what:

Bayesian graph logic: Alex, Andy, Bruno
Database: Alex, Miles, Will
Front end: Jose, Max, Will
User: Max, Qi

# Changes:

We first intended to use one huge graph to calculate cpds, but that ended up taking too long to use.
Our solution was to split the big graph up into mini graphs each composed of 1 symptom per graph with
all the relevant sub symptoms and conditions related to it. These smaller graphs calculate the cpds
much faster, and are stored in a global dictionary called "graph_dict". Each entry is of the format
{sympt_id : [Graph, sub_symptoms, conditions]}. When a user enters their initial symptom, we choose
the appropriate graph through this global dict, and evaluate as we have before.

We also added functions followup() and followup2(), which ask follow up questions depending on the
initial evaluate. From the highest probability condition chosen from the initial evaluate, the user's
presented with its related symptoms, and subsequent sub-symptoms. Unfortunately because we don't use
the total graph, we can't use the big comprehensive cpd to compute the new probability. So instead
we take the averages of the probabilities of that specific condition across all symptoms asked.

With this approach we don't have to change the database, and it's quick to start up and load. It
also uses a bit of machine learning via the Bayesian estimators, which are currently set to 100
random samples, but with more user input and verified conditions, the graph's accuracy improves.

---------------------------------------------------------------------------------------------------

## Archived notes from iteration 1:

Suggested Acceptance Testing:

As iteration 1 deals only with the high-level design and process of our application,
we have yet to populate our database (and thus our graph) with valid symptoms and conditions.
However, you can still create a username and password, login, and begin the questioning
process with our placeholder symptoms and conditions.

Implementation Overview:

In this iteration we tackled the most basic instance of start_assessment. We also built the
first draft of our front end, created the framework for our database, and built an early version
of Vida's Bayesian graph modeling

Who did what:

Bayesian graph logic: Andy, Bruno, Qi
Database: Alex, Miles
Front end: Jose, Max, Will

Changes:

From the front end perspective, we decided against Django and moved to Flask for our framework,
due to its greater flexibility and lower learning curve. Flask also provides tools for handling
users that we found effective and easy to use. As a result, we've decided to split our original
conception for the User class in two. The first part of the class, allowing Users to login and
be identified within the system, is given to Flask. While the second part of the class, storing
user health data for use in identifying their condition, will be given to the database. This
change also meant that start_assessment() is now called by the front end instead of a User class.

+----------+                     +---------------------+                     +---------------+
|   User   | <-----------------> |   Flask/Front End   | <-----------------> | Bayesian Graph |
+----------+                     +---------------------+                     +---------------+

This move is in line with a larger move of information modeling out of classes in the application,
and into the database. Since conditions and symptoms are static information, it didn't make sense
to make them into classes as we had originally intended. Instead, we store this information in
the database, and pull it when creating our graph.

This leads to our next major design change. In our original plan we had the idea to use a graph of
connected symptoms and conditions, and the probabilities of their relations to come up with an
accurate diagnosis. But we didn't realize the true complexity and challenge of this problem. So in
order to create a mathematically robust and correct solution we decided to use a Bayesian graph:
a directed acyclic graph with conditional probability distributions in each node. So even though
the graph node/edge structure is static the conditional probabilities change based on how we
traverse the graph in each assessment. This graph is built from the entries in the database.

Others:

We no longer unit test the graph explicitly, since its tested implicitly  by the success or failure
of the assessment.

We were theoretically able to get info from database into Bayesian model. However, because of how the
Bayesian model works conditional probabilities increase exponentially given connections. This means
that using the whole database as it is now takes way too long to create the graph. For the database
transition to work we would have to use a much smaller database with fewer conditions in order for
the algorithm to eventually output. So in the interest of time, as we need to quickly create and
recreate the graph to develop our code, our current graph uses a small number of with the made up
symptoms/conditions. For iteration 2 we will work on making the database smaller and the code
more efficient.

Iteration 2 Plan:

Much of what we laid out in our original design document will be implemented in Iteration 2. More
specifically, we are integrating user information to hone our algorithm and diagnostics, as we
outlined in the original document. We will be fully integrating the database with our backend algorithm,
which will now run on 12 conditions and 100+ symptoms/sub symptoms. While this is not implementing the
web scraping approach that we had discussed at the very beginning, we believe that focusing on the
algorithm over taking the time to web scrape was a better use of time resources. We believe that
the set of conditions and symptoms/sub symptoms is comprehensive enough to demonstrate the complexity
of our algorithm, and allows for a more fully formed web app to be implemented at the end of iteration 2.

We will be restructuring the database to capture relationships between symptoms and sub symptoms in order
to be able to integrate it with the updated algorithm seemlessly. Each subsymptom will only relate to a
single symptom. Since we do not have large amounts of medical data to reference, or user data, we will be
 setting naive conditional probabilities for each symptom/subsymptom relationship (where the likelihood
 of a symptom to have one of its subsymptoms is 1/(number of sub symptoms)).

In this iteration we will also be implementing a profile viewer and assessment history viewer into the
User Interface. This is entirely in line with our original goals outlined in the design document. In
addition to this, we will be adding a logout function so that users can log out, and restrictions for usernames/passwords.

In this iteration, our backend algorithm will also use data from a User's profile to refine it's
diagnosis in addition to the original Bayesian model.

---------------------------------------------------------------------------------------------------

## Unit Test Cases

All test cases can be run at once by entering the test directory from your terminal and running "pytest".
The test cases are in /app/tests

** To disable pgmpy warnings, add --disable-pytest-warnings flag when running any tests **
# test_db.py

Comments within the code of this program indicate the newest section for iteration 2. The biggest change we made was restructuring how symptoms, sub symptoms, and conditions relate to each other in accordance with the Bayesian Model graph. We now have conditions relate only to sub symptoms, and sub symptoms only relate to a single symptom. We are also adding columns to the conditions table to indicate the age range of people likely to get the conditions, as well as the typical time that symptoms can be expected to last. Again, populate_db.py and generate_sub_symptoms.py are used to fill and format the database tables, but the best way to test these programs is to query the database and make sure the data is stored the way we expect it to be.

Comments in code provide more specifics as to what each tests do, but we are mainly checking to make sure sub symptoms only map to one symptom, that conditional probabilities are correct, that age ranges for conditions are correct, and that times for conditions are correct.

Please note: we are implementing several changes to the database currently, so if tests from iteration 1 are now failing because of this, that is only temporary and will be changed once the database has its final form.

To run: at commandline run "pytest test_db.py -p no:warnings"

# test_assessment.py

The new test cases within this file are located in the TestAssessmentWithUser class. These test cases will test
the new functions that are going to be used by the assessment algorithm for the 2nd iteration of the project.

The functions include: apply_user_features(), load_graph(), and load_cpds().

To run: at commandline run "pytest test_assessment.py -p no:warnings"

# test_forms.py

New test cases now check for invalid usernames and passwords during sign up within the TestSignUp class. For other
new tests, we moved a portion of the web form test methods into a superclass (TestWebForms), so that all web form
tests can add and remove users as necessary. We also added a maximum-login rate attempt test, user profile tests, and
logout tests in TestLogin, TestProfile, and TestLogout, respectively.

These tests cover aspects for assuring valid user profile information  is entered, usernames and passwords are standardized,
and insuring that our website is not susceptible to brute-force attacks.

** Valid Edit Profile Testing is now done by using the UI in order to maintain User Session context **

To run: at commandline enter "pytest test_forms.py -p no:warnings"

# test_user.py
We re-define the backend user class to have three layers of profile information: account information, basic information, personal information, and health background.
The account information has the username and password. The basic and personal information have the user's height, weight, etc. The health background class stores information about the user's health condition, for example, whether or not the user smokes. The tests cover getting and setting information in those classes.

The user class interacts with the user schema. We refactor the user information we retrieve from the database as user schema to differentiate the user class. We will convert the user schema to a user class with getters and setters so that the backend assessment algorithm can interact with the data in the class, for example, using user age in the diagnosis.

To run: at commandline enter "pytest test_user.py -p no:warnings"

