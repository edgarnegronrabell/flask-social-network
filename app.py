from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user, 
						login_required)

from forms import RegisterForm, LoginForm
from models import DoesNotExist, User, DATABASE, initialize

app = Flask(__name__)
app.secret_key = 'adfhgsbdyfshf84ye78rih8re98m0,sf&4he.3838r43434'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	try:
		return User.get(User.id == user_id)
	except DoesNotExist:
		return None


@app.before_request
def before_request():
	"""Connect to the database before each request."""
	g.db = DATABASE
	g.db.connect()


@app.after_request
def after_request(response):
	"""Close the database connection after each request."""
	g.db.close()
	return response


@app.route('/register', methods=('GET', 'POST'))
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		flash("You have successfully registered!", "is-success has-text-centered")
		User.create_user(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data
		)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/login',  methods=('GET', 'POST'))
def login():
	form = LoginForm()
	if form.validate_on_submit():
		try:
			user = User.get(User.email == form.email.data)
		except DoesNotExist:
			flash("Your email or password don't match!", "is-danger has-text-centered")
		else:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				flash("You've been logged in!", "is-success has-text-centered")
				return redirect(url_for('index'))
			else:
				flash("Your email or password don't match!", "is-danger has-text-centered")
	return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out!", "is-success has-text-centered")
	return redirect(url_for('index'))


@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	initialize()
	try:
		User.create_user(
			username='edgarnegronrabell',
			email='edgar.negron.rabell@gmail.com',
			password='723bruhc98#*#B',
			admin=True
	)
	except ValueError:
		pass
	app.run(debug=True)