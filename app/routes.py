from app import app
from flask import render_template, jsonify, request, json
from flask_login import login_required
from app.forms import LoginForm
from .assessment import assessment

@app.route("/assessment", methods=["POST"])
def handle_assessment():
    symptom = request.form.get('data')
    successors = assessment.start_assessment(symptom)
    print(successors)
    return jsonify({'text': 'Hello World'})

@app.route("/assessment")
def symptom_assessment():
    return render_template("assessment.html")

@app.route("/", methods=["GET","POST"])
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


if __name__ == "__main__":
    app.run()
