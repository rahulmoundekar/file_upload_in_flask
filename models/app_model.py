from db.db import db
import datetime


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
