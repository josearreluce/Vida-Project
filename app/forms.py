from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, RadioField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Regexp, NumberRange, Optional
from app.models import UserSession


class ProfileForm(FlaskForm):
    age = IntegerField(
            'Age',
            validators=[Optional(),NumberRange(min=10, max=150, message="Invalid age: 10-150")],
            default='')
    sex = RadioField(
            'Sex',
            choices=[(1,' Male '),(2,' Female '), (0,' Other ')],
            validators=[Optional()],
            default=-1)
    height = IntegerField(
            'Height (Inches)',
            validators=[Optional(),NumberRange(min=30, max=110, message="Invalid height: 30-110 (inches)")],
            default='')
    weight = IntegerField(
            'Weight (Pounds)',
            validators=[Optional(),NumberRange(min=40, max=1500, message="Invalid weight: 40-1500 (lbs)")],
            default='')
    smoker = FloatField(
            'Smoker (Packs per Day)',
            validators=[Optional(),NumberRange(min=0.0, max=4.0, message="Invalid packs smoked: 0.0-4.0 (packs)")],
            default=0.0)
    blood_pressure_systolic = IntegerField(
            'Blood Pressure (High / Low mmHg)',
            validators=[Optional(), NumberRange(min=80, max=150, message="Invalid blood pressure: 80-150 (mm Hg)")],
            default='')
    blood_pressure_diastolic = IntegerField(
            '',
            validators=[Optional(), NumberRange(min=50, max=100, message="Invalid blood pressure: 50-100 (mm Hg)")],
            default='')
    diabetes = RadioField(
            'Diabetes',
            choices = [(1,' Type I   '),(2,' Type II   '), (0,' None ')],
            validators=[Optional()],
            default=-1)
    submit = SubmitField('Save')
    log_errors = [[], 0]



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    log_errors = [[], 0]


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=50, message='Invalid Username Length!'),
        Regexp('^[A-Za-z0-9]+$', message='Invalid Username: alphanumeric input only')])
    #wtforms.validators.Regexp(regex, flags=0, message=u'Invalid input.')
    password = PasswordField(
            'Password',
            validators=[DataRequired(), Length(min=4, max=50, message='Invalid Password Length!'),
            Regexp('^[A-Za-z0-9]+$', message='Invalid Password: alphanumeric input only')])
    password2 = PasswordField(
            'Repeat Password',
            validators=[DataRequired(), EqualTo('password', message='Password Must Match!')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = UserSession.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username Already In Use!')

    def validate_password(self, password):
        if self.username.data == password.data:
            raise ValidationError('Username Cannot Equal Password!')


class LogoutForm(FlaskForm):
    submit = SubmitField('Logout')
