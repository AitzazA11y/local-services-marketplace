import os
from flask import Flask, render_template, abort, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RequestForm, RegisterForm, LoginForm
from models import db, Service, ServiceRequest, User
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def home():
    all_services = Service.query.all()
    return render_template('home.html', services=all_services)

def get_service_or_404(service_id):
    return db.get_or_404(Service, service_id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/service/<int:service_id>')
def service_detail(service_id):
    service = get_service_or_404(service_id)
    return render_template('service_detail.html', service=service)

@app.route('/requests')
@login_required
def view_requests():
    entries = ServiceRequest.query.order_by(ServiceRequest.id.desc()).all()
    return render_template('requests.html', entries=entries)

from sqlalchemy.exc import SQLAlchemyError

@app.route('/service/<int:service_id>/request', methods=['GET', 'POST'])
@login_required
def request_service(service_id):
    service = get_service_or_404(service_id)
    form = RequestForm()
    if form.validate_on_submit():
        new_request = ServiceRequest(
            client_name=form.client_name.data,
            contact=form.contact.data,
            message=form.message.data,
            service_id=service.id,
        )
        try:
            db.session.add(new_request)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash("Something went wrong saving your request. Please try again.")
            return render_template('request_form.html', form=form, service=service)
        flash(f"Your request was sent to {service.provider}.")
        return redirect(url_for('service_detail', service_id=service.id))
    return render_template('request_form.html', form=form, service=service)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('That email is already registered.')
            return render_template('register.html', form=form)
        flash('Account created. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password.')
            return render_template('login.html', form=form)
        login_user(user)
        flash(f'Welcome back, {user.name}.')
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)