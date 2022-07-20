from __init__ import db
import time
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import PasswordField, StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegisterTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_time = db.Column(db.Integer)
    username = db.Column(db.String(80), db.ForeignKey(Customer.username))

    def __init__(self, username):
        self.username = username
        self.register_time = time.time()


class LoginTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_time = db.Column(db.Integer)
    username = db.Column(db.String(80), db.ForeignKey(Customer.username))

    def __init__(self, username):
        self.username = username
        self.login_time = time.time()


class RegistrationForm(FlaskForm):
    first_name = StringField('Firstname:', validators=[DataRequired()])
    last_name = StringField('Lastname:', validators=[DataRequired()])
    username = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Register')


class UploadForm(FlaskForm):
    photo_coat = FileField('image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    photo_shirt = FileField('image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    photo_trousers = FileField('image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Finished')


class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()
#
#
# class SimpleForm(FlaskForm):
#     string_of_files = ['one\r\ntwo\r\nthree\r\n']
#     list_of_files = string_of_files[0].split()
#     # create a list of value/description tuples
#     files = [(x, x) for x in list_of_files]
#     example = MultiCheckboxField('Label', choices=[False, True])
