from app import app
from flask import render_template, jsonify
from flask_login import login_required
from app.forms import LoginForm, SignUpForm
import sqlalchemy as sqlalchemy
from sqlalchemy.orm import sessionmaker
from app.src.db_user import User
from flask import request
from flask import redirect

@app.route("/assessment", methods=["POST"])
def handle_assessment():
    return jsonify({'text': 'Hello World'})

@app.route("/assessment")
def symptom_assessment():
    return render_template("assessment.html")

@app.route("/", methods=["GET","POST"])
def login():
    form = LoginForm()
    username = form.username
    password = form.password
    print(form.username)
    return render_template('login.html', title='Sign In', form=form)

@app.route("/sign_up", methods=["GET","POST"])
def signup():
    form = SignUpForm(request.form)
    username = form.username.data
    password = form.password.data

    print(form.validate_on_submit())

    if form.validate_on_submit():
        engine = sqlalchemy.create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
        Session = sessionmaker()
        Session.configure(bind=engine)
        print(type(username))
        db = Session()
        user_info = User(username=username, pswd=password)
        check_user = db.query(User).filter_by(username='test').all()
        print(check_user)
        if check_user:
        	return redirect('/sign_up')
        db.add(user_info)
        db.commit()
        return redirect('/assessment')
    return render_template('sign_up.html', title='Sign Up', form=form)


if __name__ == "__main__":
    app.run()
