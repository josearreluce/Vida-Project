from app import app
from flask import render_template, jsonify
from flask_login import login_required
from app.forms import LoginForm

@app.route("/assessment", methods=["POST"])
def handle_assessment():
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
