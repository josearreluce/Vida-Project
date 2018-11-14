from app import app
from app.forms import LoginForm
from flask import render_template, jsonify, redirect, flash
from app.forms import LoginForm, SignUpForm
from flask import request
from flask import redirect
from app.models import DatabaseConnection, User
from .assessment import assessment

curr_user = 0
users = {curr_user: {}}
@app.route('/successors',methods=['GET','POST'])
def handle_successors():
    jsonData = request.get_json()
    answers = jsonData['answers']
    symptom = users[curr_user]["symptom"]
    successors = users[curr_user]["successors"]
    conditions = assessment.evaluate(symptom, successors, answers)
    return jsonify({'text':"hello world", 'conditions': conditions})

@app.route("/assessment", methods=["POST"])
def handle_assessment():
    symptom = request.form.get('data')
    users[curr_user]['symptom'] = symptom
    successors = assessment.start_assessment(symptom)
    users[curr_user]['successors'] = successors
    return jsonify({'text': 'Hello World', 'successors': successors})

@app.route("/assessment")
def symptom_assessment():
    return render_template("assessment.html")

@app.route("/", methods=["GET","POST"])
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


if __name__ == "__main__":
    app.run()
