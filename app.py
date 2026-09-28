from flask import Flask, render_template

app = Flask(__name__)

services = [
    {"id": 1, "title": "Home Plumbing Repair", "category": "Plumber", "provider": "Ahmed Hassan", "price": "Rs. 1500"},
    {"id": 2, "title": "Electrical Wiring Fix", "category": "Electrician", "provider": "Bilal Khan", "price": "Rs. 2000"},
    {"id": 3, "title": "Math Tutoring (O/A Levels)", "category": "Tutor", "provider": "Sana Malik", "price": "Rs. 800/hr"},
]

@app.route('/')
def home():
    return render_template('home.html', services=services)

if __name__=='__main__':
    app.run(debug=True)