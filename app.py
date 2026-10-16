import os
from flask import Flask, render_template, abort, redirect, url_for, flash
from forms import RequestForm, RegisterForm
from models import db, Service, ServiceRequest, User
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

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
def view_requests():
    entries = ServiceRequest.query.order_by(ServiceRequest.id.desc()).all()
    return render_template('requests.html', entries=entries)

from sqlalchemy.exc import SQLAlchemyError

@app.route('/service/<int:service_id>/request', methods=['GET', 'POST'])
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
        flash('Account created.')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

if __name__=='__main__':
    app.run(debug=True)