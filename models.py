from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = "contacts"

    id          = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(80), nullable=False)
    last_name   = db.Column(db.String(80), nullable=False)
    email       = db.Column(db.String(120), nullable=False, unique=True)
    phone       = db.Column(db.String(20))
    company     = db.Column(db.String(120))
    address     = db.Column(db.String(200))
    category    = db.Column(db.String(20), default="personal")
    notes       = db.Column(db.Text)
    is_favorite = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "firstName":   self.first_name,
            "lastName":    self.last_name,
            "email":       self.email,
            "phone":       self.phone or "",
            "company":     self.company or "",
            "address":     self.address or "",
            "category":    self.category,
            "notes":       self.notes or "",
            "favourite":   self.is_favorite,
            "created":     int(self.created_at.timestamp() * 1000),
        }
