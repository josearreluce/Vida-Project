from app import app

from flask import render_template, jsonify, redirect, flash
from flask_login import login_required
from app.forms import LoginForm, SignUpForm
import sqlalchemy as sqlalchemy
from sqlalchemy.orm import sessionmaker
from flask import request
from flask import redirect
from app.models import DatabaseConnection, UserSchema
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

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == '' or password == '':
            if form.log_errors:
                form.log_errors.pop()
            form.log_errors.append('Username and Password Must Be Filed In')
            return redirect('/')

        with DatabaseConnection() as db:
            user_info = UserSchema(username=username, pswd=password)
            check_user = db.query(UserSchema).filter_by(username=username, pswd=password).count()

        if check_user < 1:
            if form.log_errors:
                form.log_errors.pop()
            flash('Failed login!')
            form.log_errors.append('Invalid Username or Password')
            return redirect('/')
        elif check_user > 1:
            if form.log_errors:
                form.log_errors.pop()
            form.log_errors.append('DATABASE ERROR PLEASE CONTACT ADMINS')
            return redirect('/')
        else:
            if form.log_errors:
                form.log_errors.pop()
            return redirect('/assessment')

    return render_template('login.html', title='Log In', form=form)


@app.route("/sign_up", methods=["GET","POST"])
def signup():
    form = SignUpForm(request.form)
    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():

        with DatabaseConnection() as db:
            user_info = UserSchema(username=username, pswd=password)
            check_user = db.query(UserSchema).filter_by(username=username).all()

        if check_user:
            if form.log_errors:
                form.log_errors.pop()
            form.log_errors.append('Username "{}" Already In Use!'.format(username))
        else:
            flash('Welcome to Vida!')
            db.add(user_info)
            db.commit()
            if form.log_errors:
                form.log_errors.pop()
            return redirect('/assessment')

    return render_template('sign_up.html', title='Sign Up', form=form)


if __name__ == "__main__":
    app.run()
