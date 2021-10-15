from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class Keys(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    api_key = database.Column(database.String(20), nullable=False)
    email = database.Column(database.String(100), nullable=False, unique=True)
    timestamp = database.Column(database.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Api_key %r>' % self.api_key
