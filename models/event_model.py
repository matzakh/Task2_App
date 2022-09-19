from db import db
from flask import jsonify
from collections import namedtuple
from enum import IntEnum


class EventType(IntEnum):
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


class EventStatus(IntEnum):
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
    scheduled_start = db.Column(db.DATETIME, nullable=True)
    actual_start = db.Column(db.DATETIME, nullable=True)

    def __init__(self, name, slug, active, type, sport, status, scheduled_start=None, actual_start=None):
        self.name = name
        self.slug = slug
        self.active = active
        if isinstance(type, str):
            type = EventType.str_to_int(type)
        self.type = type
        if isinstance(sport, str):
            # sport query here
            sport = sport
        self.sport = sport
        if isinstance(status, str):
            status = EventStatus.str_to_int(status)
        self.status = status
        self.scheduled_start = scheduled_start
        self.actual_start = actual_start

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

    def save_to_db(self):
        db.session.execute("""INSERT INTO events (name, slug, active, type, sport, status, scheduled_start, actual_start) 
                              VALUES ('{0}', '{1}', {2}, {3}, {4}, {5}, {6}, {7})""".format(self.name,
                                                                                            self.slug,
                                                                                            self.active,
                                                                                            self.type,
                                                                                            self.sport,
                                                                                            self.status,
                                                                                            self.scheduled_start,
                                                                                            self.actual_start))
        db.session.commit()

    @classmethod
    def find_by_params(cls, **kwargs):
        matched_models = []
        filter_str = ''

        for key, value in kwargs.items():
            val = value[0]
            if key == 'name' or key == 'slug':
                filter_str += str(key) + ' REGEXP "' + str(val) + '"'
            elif val.lower() == 'true':
                filter_str += str(key)
            elif val.lower() == 'false':
                filter_str += 'not ' + str(key)
            elif key == 'type':
                filter_str += str(key) + '=' + str(EventType.str_to_int(val))
            elif key == 'status':
                filter_str += str(key) + '=' + str(EventStatus.str_to_int(val))
            else:
                filter_str += str(key) + '=' + str(val)
            filter_str += ' and '

        filter_str = filter_str[:-5]

        result = db.session.execute('SELECT * FROM events WHERE ' + filter_str)
        Record = namedtuple('Record', result.keys())
        records = [Record(*r) for r in result.fetchall()]

        for r in records:
            matched_models.append(EventModel(name=r.name,
                                             slug=r.slug,
                                             active=r.active,
                                             type=r.type,
                                             sport=r.sport,
                                             status=r.status,
                                             scheduled_start=r.scheduled_start,
                                             actual_start=r.actual_start)._assign_id(r.id))

        return matched_models

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
