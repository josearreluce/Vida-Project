from app import app
from flask import render_template, jsonify, redirect, flash
from flask_login import login_required
from app.forms import LoginForm, SignUpForm
import sqlalchemy as sqlalchemy
from sqlalchemy.orm import sessionmaker
from flask import request
from flask import redirect
from app.models import DatabaseConnection, User


@app.route("/assessment", methods=["POST"])
def handle_assessment():
    return jsonify({'text': 'Hello World'})


@app.route("/assessment")
def symptom_assessment():
    return render_template("assessment.html")


@app.route("/", methods=["GET","POST"])
def login():
    form = LoginForm()

    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():

        with DatabaseConnection() as db:
            user_info = User(username=username, pswd=password)
            check_user = db.query(User).filter_by(username=username, pswd=password).count()

        if check_user < 1:
            if form.errors:
                form.errors.pop()
            form.errors.append('Invalid Username or Password')
            return redirect('/')
        elif check_user > 1:
            if form.errors:
                form.errors.pop()
            form.errors.append('DATABASE ERROR PLEASE CONTACT ADMINS')
            return redirect('/')
        else:
            if form.errors:
                form.errors.pop()
            return redirect('/assessment')

    return render_template('login.html', title='Log In', form=form)


@app.route("/sign_up", methods=["GET","POST"])
def signup():
    form = SignUpForm(request.form)
    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():

        with DatabaseConnection() as db:
            user_info = User(username=username, pswd=password)
            check_user = db.query(User).filter_by(username=username).all()

        if check_user:
            if form.errors:
                form.errors.pop()
            form.errors.append('Username "{}" Already In Use!'.format(username))
        else:
            flash('Welcome to Vida!')
            db.add(user_info)
            db.commit()
            if form.errors:
                form.errors.pop()
            return redirect('/assessment')

    return render_template('sign_up.html', title='Sign Up', form=form)


if __name__ == "__main__":
    app.run()
