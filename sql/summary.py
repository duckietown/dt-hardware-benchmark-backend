from sql import db
import datetime

class Summary(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    uuid = db.Column(db.String(64), unique=True, nullable=False)
    bot_type = db.Column(db.String(64), nullable=False)
    battery_type = db.Column(db.String(64), nullable=False)
    release = db.Column(db.String(64), nullable=False)
    target = db.Column(db.String(64), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    overall = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Summary %r>' % self.uuid