from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import sqlalchemy as sqlalchemy
from sqlalchemy.orm import sessionmaker
from app.src.db_user import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    #db = sqlalchemy.create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    # engine = sqlalchemy.create_engine("postgresql://pv_admin:CMSC22001@ec2-13-59-75-157.us-east-2.compute.amazonaws.com:5432/pv_db")
    # Session = sessionmaker()
    # Session.configure(bind=engine)
    # print(type(username))
    # db = Session()
    # user_info = User(username=username, password=password)
    # db.add(user_info)
    # db.commit()