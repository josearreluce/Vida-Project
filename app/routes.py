from app import app
from flask import render_template
from app.forms import LoginForm

@app.route("/assessment")
def symptom_assessment():
    return render_template("assessment.html")

@app.route("/")
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


if __name__ == "__main__":
    app.run()
