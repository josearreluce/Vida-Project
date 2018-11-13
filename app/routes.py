from app import app
from flask import render_template, jsonify, request, json
from flask_login import login_required
from app.forms import LoginForm
from .assessment import assessment

curr_user = 0
users = {curr_user: {}}
"""
@app.route("/successors", methods=["POST"])
def handle_successors():
    print("Assessments")
    #answers = request.form.get('data')
    print(request.form)
    #print(request.get_json())
    #answers = request.get_json()
    #print("answers: ", answers)
    # symptom = users[curr_user]["symptom"]
    # print("symp ", symptom)
    # successors = users[curr_user]["successors"]
    # print("3 ", successors)
    # conditions = assessment.evaluate(symptom, successors, answers)
    # print("4 ", conditions)
    
    return jsonify({'text': 'Hello World 2', 'conditions': 'cond' })
"""
@app.route('/successors',methods=['GET','POST'])
def handle_successors():
    jsonData = request.get_json()
    answers = jsonData['answers']
    symptom = users[curr_user]["symptom"]
    successors = users[curr_user]["successors"]
    conditions = assessment.evaluate(symptom, successors, answers)
    #print(jsonData['age'])
    return jsonify({'text':"hello world", 'conditions': conditions}) #or whatever you want to return

@app.route("/assessment", methods=["POST"])
def handle_assessment():
    print("Handling Assessment")
    symptom = request.form.get('data')
    print(symptom)
    users[curr_user]['symptom'] = symptom
    print("Symptom returned " + symptom)
    successors = assessment.start_assessment(symptom)
    users[curr_user]['successors'] = successors
    print(jsonify(successors))
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
