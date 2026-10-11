from app import app
from models import db, Service

SERVICES = [
    {"title": "Home Plumbing Repair", "category": "Plumber", "provider": "Ahmed Hassan", "price": "Rs. 1500"},
    {"title": "Electrical Wiring Fix", "category": "Electrician", "provider": "Bilal Khan", "price": "Rs. 2000"},
    {"title": "Math Tutoring (O/A Levels)", "category": "Tutor", "provider": "Sana Malik", "price": "Rs. 800/hr"},
]

with app.app_context():
    if Service.query.count() == 0:
        for data in SERVICES:
            db.session.add(Service(**data))
        db.session.commit()
        print("Seeded", len(SERVICES), "services")
    else:
        print("Services already exist, skipping")