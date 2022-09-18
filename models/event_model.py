from db import db
from flask import jsonify
from collections import namedtuple
from enum import Enum


class EventType(Enum):
    PREPAY = 1
    INPLAY = 2

    @classmethod
    def str_to_int(cls, str_val):
        if str_val.lower() == 'prepay':
            return cls.PREPAY
        elif str_val.lower() == 'inplay':
            return cls.INPLAY
        else:
            return None


class EventStatus(Enum):
    PENDING = 1
    STARTED = 2
    ENDED = 3
    CANCELLED = 4

    @classmethod
    def str_to_int(cls, str_val):
        if str_val.lower() == 'pending':
            return cls.PENDING
        elif str_val.lower() == 'started':
            return cls.STARTED
        elif str_val.lower() == 'ended':
            return cls.ENDED
        elif str_val.lower() == 'cancelled':
            return cls.CANCELLED
        else:
            return None


class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean)
    type = db.Column(db.Integer, nullable=False)
    sport = db.Column(db.Integer, db.ForeignKey('sports.id'))
    status = db.Column(db.Integer, nullable=False)
    scheduled_start = db.Column(db.DATETIME)
    actual_start = db.Column(db.DATETIME)

    def __repr__(self):
        return "<Event %r>" % self.name

    def _assign_id(self, id):
        self.id = id
        return self

    def json(self):
        return jsonify({
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'active': self.active,
            'type': self.type,
            'sport': self.sport,
            'status': self.status,
            'scheduled_start': self.scheduled_start,
            'actual_start': self.actual_start
        })

    @classmethod
    def find_by_field(cls, field_value, field_name='slug'):
        if isinstance(field_value, str):
            field_value = '"' + field_value + '"'
        if field_name == 'type':
            field_value = EventType.str_to_int(field_value)
        elif field_name == 'status':
            field_value = EventStatus.str_to_int(field_value)
        result = db.session.execute('SELECT * FROM events WHERE {0} = {1} LIMIT 1'.format(field_name, field_value))
        Record = namedtuple('Record', result.keys())
        records = [Record(*r) for r in result.fetchall()]
        for r in records:
            return EventModel(name=r.name,
                              slug=r.slug,
                              active=r.active,
                              type=r.type,
                              sport=r.sport,
                              status=r.status,
                              scheduled_start=r.scheduled_start,
                              actual_start=r.actual_start)._assign_id(r.id)
