"""Database Model for Summary"""
import datetime
from sql import db


class Summary(db.Model):
    """Definition of DB-Model"""
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False)
    bot_type = db.Column(db.String(64), nullable=False)
    battery_type = db.Column(db.String(64), nullable=False)
    release = db.Column(db.String(64), nullable=False)
    target = db.Column(db.String(64), nullable=False)
    created = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        nullable=False)
    summary = db.Column(db.Text, nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Summary %r>' % self.uuid
