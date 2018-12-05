# Vida-Project
# Authors: Jose Arreluce, Alex Bai, Will Darling, Max Demers, Miles Grogger, Andy Ham, Bruno Jacob, Qi Jin
## Original repo: "https://github.com/josearreluce/Vida-Project.git"

---------------------------------------------------------------------------------------------------

# Preface

The internet has become a diagnosis tool for potential health issues for people experiencing symtoms.
However, the user is faced with an overwhelming amount of diagnoses, some ambiguous, some severe, and none
of them personalized. <br/>
Vida attempts to solve these problems by providing a personalized and intuitive symptom assessment experience, using user health information for an accurate diagnosis.

---------------------------------------------------------------------------------------------------

# Installation Guide

Please run the below setup in your terminal. Dependencies can be readily installed on Linux and Mac terminals/

```
$ git clone https://github.com/josearreluce/Vida-Project.git
$ cd Vida-Project
$ pip3 install -r requirements.txt
$ python3 -m flask run
```

Navigate to http://127.0.0.1:5000/ in your browser to access the web application.

NOTE: Please run our application in Firefox.
(Our application is supported across platforms, but please use Firefox or Safari for best results.)

---------------------------------------------------------------------------------------------------

# Tutorial

We designed Vida to be intuitive to navigate and use. <br/>
We recommend that the user sign-up and create a profile. While this isn't required to start an assessment, it's highly recommended for a more personalized and accurate diagnosis. Access your profile by clicking on "Profile" and "Edit info" to add in your health background. <br/>
Begin an assessment by going to "Begin Assessment". Enter the most prominent symptom you are experiencing
in the search bar and select the matching entry. You will be asked a series of follow-up questions for Vida to better understand your symptoms and provide you with a diagnosis. <br/>
Vida currently supports 12 starting symptoms (please see a full list in the appendix).

---------------------------------------------------------------------------------------------------

# Running the Unit Tests

The UI Tests require an additional dependency. <br/>
Download a chrome webdriver from http://chromedriver.chromium.org/downloads
and place the driver into the test directory. <br/>

Then run the following from the /tests directory
```
$ pytest -p no:warnings
```

NOTE: Please consult the appendix for a thorough guide on tests.

---------------------------------------------------------------------------------------------------

# Poorly Handled Inputs

Top level symptoms "Dilated Pupils" and "Diarrhea" are not handled as well as other symptoms.

---------------------------------------------------------------------------------------------------
# Implementation Overview

In this final round of development we greatly improved the functionality around user profile
information. When adding information, a single error in one field will not erase all changes from
that session, and there are more stringent checks to prevent users from entering unrealistic data.
We also added password salting for improved security. Finally, the user's health information is
properly implemented in the assessment process. At the end of the questionaire, the probabilities
are filtered based on the user information before a final diagnosis is reached.

---------------------------------------------------------------------------------------------------

# Appendix 

## Supported Conditions

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

## Supported Top Level Symptoms (these are the only symptoms that begin an assessment)

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

