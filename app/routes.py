from app import app, db
from flask import render_template, jsonify, redirect
from flask_login import login_required, login_user, current_user, logout_user
import sqlalchemy as sqlalchemy
from sqlalchemy.orm import sessionmaker
from flask import request
from flask import redirect
from wtforms.validators import ValidationError
from app.models import DatabaseConnection, UserSession
from app.forms import LoginForm, SignUpForm, LogoutForm
from .assessment import assessment

@app.route('/profile', methods=['GET', 'POST'])
def view_profile():
    return render_template("profile.html")

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

    if current_user.is_authenticated:
         if form.log_errors:
                form.log_errors.pop()
            form.log_errors.append('Already Logged In!!')
        return redirect('/profile')


    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        check_user = UserSession.query.filter_by(username=username).first()
        if check_user is None or not check_user.check_password(password):
            if form.log_errors:
                form.log_errors.pop()
            form.log_errors.append('Invalid Username or Password!')
            return redirect('/')
        else:
            login_user(check_user, remember=form.remember_me.data)
            return redirect('/assessment')

    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    form = LogoutForm()

    if form.submit():
        logout_user()
    return redirect('/')


@app.route("/sign_up", methods=["GET","POST"])
def signup():
    form = SignUpForm(request.form)
    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():

        user = UserSession(username=username, pswd=password)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return redirect('/assessment')

    return render_template('sign_up.html', title='Sign Up', form=form)


if __name__ == "__main__":
    app.run()
