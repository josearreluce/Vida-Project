from app import app, db
from flask import render_template, jsonify, redirect
from flask_login import login_required, login_user, current_user, logout_user
import sqlalchemy as sqlalchemy
from sqlalchemy.orm import sessionmaker
from flask import request
from flask import redirect, url_for
from wtforms.validators import ValidationError
from app.models import DatabaseConnection, UserSession
from app.forms import LoginForm, SignUpForm, LogoutForm, ProfileForm
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
    all_symptoms = assessment.get_all_symptoms()
    # print(all_symptoms)
    symptom = request.form.get('data')
    users[curr_user]['symptom'] = symptom
    successors = assessment.start_assessment(symptom, current_user)
    users[curr_user]['successors'] = successors
    return jsonify({'text': 'Hello World', 'successors': successors})

@app.route('/profile', methods=['GET', 'POST'])
def view_profile():
    form = ProfileForm()

    form.sex.data = int(form.sex.data)
    form.diabetes.data = int(form.diabetes.data)

    if form.validate_on_submit():
        user = UserSession.query.get(current_user.username)
        if form.age.data != '':
            user.age = form.age.data
        if form.sex.data != '-1':
            user.sex = form.sex.data
        if form.height.data != '':
            user.height = form.height.data
        if form.weight.data != '':
            user.weight = form.weight.data
        if form.smoker.data != 0:
            user.smoker = form.smoker.data
        if form.blood_pressure_systolic != '' and form.blood_pressure_diastolic.data != '':
            user.blood_pressure_systolic = form.blood_pressure_systolic.data
            user.blood_pressure_diastolic = form.blood_pressure_diastolic.data
        if form.diabetes.data != -1:
            user.diabetes = form.diabetes.data

        db.session.commit()
        return render_template("profile.html", form=form)

    return render_template("profile.html", form=form)


@app.route("/assessment")
def symptom_assessment():
    return render_template("assessment.html")

@app.route("/assessment_history")
def handle_assessment_history():
    return render_template("assessment_history.html")


@app.route("/", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.log_errors[1] > 4:
        return redirect('/failed') # Prevent Brute Force Attacks

    if not current_user.is_authenticated and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        check_user = UserSession.query.filter_by(username=username).first()
        if check_user is None or not check_user.check_password(password):
            if form.log_errors[0]:
                form.log_errors[0].pop()

            form.log_errors[0].append('Invalid Username or Password!')
            form.log_errors[1] += 1

            return redirect('/')
        else:
            if form.log_errors[0]:
                form.log_errors[0].clear()

            form.log_errors[1] = 0
            login_user(check_user, remember=form.remember_me.data)

        return redirect('/assessment')

    return render_template('login.html', title='Log In', form=form)


@app.route("/failed")
def failed():
    return render_template("failed.html")


@app.route('/logout')
@login_required
def logout():
    form = LogoutForm()
    if form.submit():
        logout_user()
    return redirect('/')


@app.route("/sign_up", methods=["GET","POST"])
def signup():
    form = SignUpForm(request.form)

    if form.validate_on_submit() and not current_user.is_authenticated:

        username = form.username.data
        password = form.password.data
        user = UserSession(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        login_user(user)

        return redirect('/assessment')

    return render_template('sign_up.html', title='Sign Up', form=form)


if __name__ == "__main__":
    app.run()
