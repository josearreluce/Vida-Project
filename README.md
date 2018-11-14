# Vida-Project
# Authors: Jose Arreluce, Will Darling, Max Demers, Miles Grogger, Andy Ham, 
           Bruno Jacob, Thomas Jacobs, Qi Jin
# Original repo: "https://github.com/josearreluce/Vida-Project.git"

# Preface
Vida attempts to solve the problem of online health condition diagnosis. The web
application begins by first asking the user for their most notable symptoms, then
continuing to ask further follow-up and clarifying questions about their condition
and potentially relevant, recent behavior and actions (i.e. starting a new medicine,
trying new food, etc.). In combination with baseline health information supplied by
the user (weight, diet, etc.) Vida provides a more specific and accurate diagnosis
than a quick search on Google or WebMD.

# Course specified entries 

(1) how to compile
$ git clone https://github.com/josearreluce/Vida-Project.git
$ pip3 install -r requirements.txt 

---------------------------------------------------------------------------------------------------

(2) how to run your code
From within the Vida-Project directory run:
$ python3 -m flask run
Then navigate to the specified port in your browser

---------------------------------------------------------------------------------------------------

(3) how to run the unit test cases
First download a chrome webdriver from http://chromedriver.chromium.org/downloads
The UI Tests require downloading this webdriver.

Then from within the tests directory run
$ pytest

---------------------------------------------------------------------------------------------------

(4) please suggest some acceptance tests for the TA to try (i.e., what inputs to use,
    and what outputs are expected)
As iteration 1 deals only with the high-level design and process of our application, 
we have yet to populate our database (and thus our graph) with valid symptoms and conditions.
However, you can still create a username and password, login, and begin the questioning
process with our placeholder symptoms and conditions.

---------------------------------------------------------------------------------------------------

(5) text description of what is implemented. You can refer to the use cases and user stories 
    in your design document.
In this iteration we tackled the most basic instance of start_assessment. We also built the 
first draft of our front end, created the framework for our database, and built an early version
of Vida's Baysian graph modeling

---------------------------------------------------------------------------------------------------

(6) who did what: who paired with who; which part is implemented by which pair
Baysian graph logic: Andy, Bruno, Qi
Database: Alex, Miles
Front end: Jose, Max, Will

---------------------------------------------------------------------------------------------------

(7) changes: have you made any design changes or unit test changes from earlier milestones?

From the front end perspective, we decided against Django and moved to Flask for our framework, 
due to its greater flexibility and lower learning curve. Flask also provides tools for handling 
users that we found effective and easy to use. As a result, we've decided to split our original
conception for the User class in two. The first part of the class, allowing Users to login and
be identified within the system, is given to Flask. While the second part of the class, storing
user health data for use in identifying their condition, will be given to the database. This
change also meant that start_assessment() is now called by the front end instead of a User class.

+----------+                     +---------------------+                     +---------------+
|   User   | <-----------------> |   Flask/Front End   | <-----------------> | Baysian Graph |
+----------+                     +---------------------+                     +---------------+

This move is in line with a larger move of information modeling out of classes in the application,
and into the databse. Since conditions and symptoms are static information, it didn't make sense
to make them into classes as we had originally intended. Instead, we store this information in
the database, and pull it when creating our graph.  

This leads to our next major design change. In our original plan we had the idea to use a graph of connected symptoms and conditions, and the probabilities of their relations to come up with an accurate diagnosis. But we didn't realize the true complexity and challenge of this problem. So in order to create a mathematically robust and correct solution we decided to use a Baysian graph: a directed acyclic graph with conditional probability distributions in each node. So even though the graph node/edge structure is static the conditional probabilities change based on how we traverse the graph in each assessment. This graph is built from the entries in the database.

---------------------------------------------------------------------------------------------------

(8) others: whatever you want to let the TA know

We no longer unit test the graph explicitly, since its tested implicitly  by the success or failure 
of the assessment.

We were theoretically able to get info from database into Baysian model. However, because of how the 
Baysian model works conditional probabilities increase exponentially given connections. This means 
that using the whole database as it is now takes way too long to create the graph. For the database 
transition to work we would have to use a much smaller database with fewer conditions in order for 
the algorithm to eventually output. So in the interest of time, as we need to quickly create and 
recreate the graph to develop our code, our current graph uses a small number of with the made up 
symptoms/conditions. For iteration 2 we will work on making the database smaller and the code 
more efficient.