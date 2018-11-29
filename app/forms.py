from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, Regexp
from app.models import UserSession

class ProfileForm(FlaskForm):
    age = StringField('Age', validators=[DataRequired()])
    sex = StringField('Sex', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])
    weight = StringField('Weight', validators=[DataRequired()])
    smoker = StringField('Smoker', validators=[DataRequired()])
    blood_pressure_systolic = StringField('Blood Pressure Systolic (Higher measurement)', 
        validators=[DataRequired()])
    blood_pressure_diastolic = StringField('Blood Pressure Diastolic (Lower measurement)', 
        validators=[DataRequired()])
    diabetes = StringField('Diabetes', validators=[DataRequired()])
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    log_errors = []


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=50, message='Invalid Username Length!')])
    #wtforms.validators.Regexp(regex, flags=0, message=u'Invalid input.')
    password = PasswordField(
            'Password',
            validators=[DataRequired(), Length(min=4, max=50, message='Invalid Password Length!'), 
            Regexp('^[^0-9a-zA-Z]+$', message='Invalid Password: alphanumeric input only')])
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
