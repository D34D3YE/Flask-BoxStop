from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))


class Fahrtenbuch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    street_start = db.Column(db.String(1000))
    street_start_hnr = db.Column(db.Integer)
    street_plz_start = db.Column(db.Integer)
    street_start_ort = db.Column(db.String(200))

    street_end = db.Column(db.String(1000))
    street_end_hnr = db.Column(db.Integer)
    street_plz_end = db.Column(db.Integer)
    street_end_ort = db.Column(db.String(200))

    km_start = db.Column(db.Float(10))
    km_end = db.Column(db.Float(10))

    km_diff = db.Column(db.Float(10))


class Ausgaben(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    aus_title = db.Column(db.String(200))
    aus_value = db.Column(db.Float(20))
    aus_type = db.Column(db.String(150))
    aus_date = db.Column(db.Date)
