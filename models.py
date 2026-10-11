from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(30))

    def __repr__(self):
        return f"<Service {self.id}: {self.title}>"


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

    service = db.relationship('Service', backref='requests')