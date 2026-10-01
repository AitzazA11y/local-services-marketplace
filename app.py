from flask import Flask, render_template, abort

app = Flask(__name__)

services = [
    {"id": 1, "title": "Home Plumbing Repair", "category": "Plumber", "provider": "Ahmed Hassan", "price": "Rs. 1500"},
    {"id": 2, "title": "Electrical Wiring Fix", "category": "Electrician", "provider": "Bilal Khan", "price": "Rs. 2000"},
    {"id": 3, "title": "Math Tutoring (O/A Levels)", "category": "Tutor", "provider": "Sana Malik", "price": "Rs. 800/hr"},
]

@app.route('/')
def home():
    return render_template('home.html', services=services)

@app.route('/service/<int:service_id>')
def service_detail(service_id):
    service = next((s for s in services if s['id'] == service_id), None)
    if service is None:
        abort(404)
    return render_template('service_detail.html', service=service)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__=='__main__':
    app.run(debug=True)