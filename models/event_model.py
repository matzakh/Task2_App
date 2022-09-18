from db import db
from flask import jsonify
from collections import namedtuple
from enum import Enum


class EventType(Enum):
    PREPAY = 1
    INPLAY = 2


class EventStatus(Enum):
    PENDING = 1
    STARTED = 2
    ENDED = 3
    CANCELLED = 4


class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean)
    type = db.Column(db.Integer)
    sport = db.Column(db.Integer, db.ForeignKey('sports.id'))
    scheduled_start = db.Column(db.DATETIME)
    actual_start = db.Column(db.DATETIME)

    def __repr__(self):
        return "<Event %r>" % self.name

    def json(self):
        return jsonify({
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'active': self.active,
            'type': self.type,
            'sport': self.sport,
            'scheduled_start': self.scheduled_start,
            'actual_start': self.actual_start
        })

