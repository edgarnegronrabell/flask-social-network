from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
								Length, EqualTo)
from models import User

def name_exists(form, field):
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('A user with that name already exists.')

def email_exists(form, field):
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('A user with that email already exists.')

class RegisterForm(FlaskForm):
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Regexp(
				r'^[a-zA-Z0-9_]+$',
				message=("Username should be one word, letters, " 
				"numbers, and underscores only.")
			),
			name_exists
		])
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email(),
			email_exists
		])
	password = PasswordField(
		'Password',
		validators=[
			DataRequired(),
			Length(min=6, max=50),
			EqualTo('confirm_password', message='Passwords must match')
		])
	confirm_password = PasswordField(
		'Confirm Password',
		validators=[DataRequired()]
	)


class LoginForm(FlaskForm):
	email = StringField(
			'Email',
			validators=[
				DataRequired(),
				Email(),
			])
	password = PasswordField(
			'Password',
			validators=[
			DataRequired(),
		])