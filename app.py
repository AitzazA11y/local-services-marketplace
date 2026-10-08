import os
from flask import Flask, render_template, abort, redirect, url_for, flash
from forms import RequestForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')

requests_list = []   # stand-in for a database table, lives in memory only

services = [
    {"id": 1, "title": "Home Plumbing Repair", "category": "Plumber", "provider": "Ahmed Hassan", "price": "Rs. 1500"},
    {"id": 2, "title": "Electrical Wiring Fix", "category": "Electrician", "provider": "Bilal Khan", "price": "Rs. 2000"},
    {"id": 3, "title": "Math Tutoring (O/A Levels)", "category": "Tutor", "provider": "Sana Malik", "price": "Rs. 800/hr"},
]

@app.route('/')
def home():
    return render_template('home.html', services=services)

def get_service_or_404(service_id):
    service = next((s for s in services if s['id'] == service_id), None)
    if service is None:
        abort(404)
    return service

@app.route('/service/<int:service_id>')
def service_detail(service_id):
    service = get_service_or_404(service_id)
    return render_template('service_detail.html', service=service)

@app.route('/service/<int:service_id>/request', methods=['GET', 'POST'])
def request_service(service_id):
    service = get_service_or_404(service_id)
    form = RequestForm()
    if form.validate_on_submit():
        requests_list.append({
            'service_id': service_id,
            'client_name': form.client_name.data,
            'contact': form.contact.data,
            'message': form.message.data,
        })
        flash(f"Your request was sent to {service['provider']}.")
        return redirect(url_for('service_detail', service_id=service_id))
    return render_template('request_form.html', form=form, service=service)

if __name__=='__main__':
    app.run(debug=True)