from db import db
from flask import jsonify
from collections import namedtuple
from enum import IntEnum
from .sport_model import SportModel
from common.utils import if_none_replace_with_strnull, parse_clauses_for_query, parse_key_val_with_operator
from datetime import datetime as dt


class EventType(IntEnum):
    PREPAY = 1
    INPLAY = 2

    @classmethod
    def str_to_int(cls, str_val):
        if not isinstance(str_val, str):
            return str_val
        if str_val.isdigit():
            return int(str_val)
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
        if not isinstance(str_val, str):
            return str_val
        if str_val.isdigit():
            return int(str_val)
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
        self.type = EventType.str_to_int(type)
        if isinstance(sport, str):
            if sport.isalpha():
                sport = SportModel.find_by_field(sport, field_name='name').id
            else:
                sport = int(sport)
        self.sport = sport
        self.status = EventStatus.str_to_int(status)
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
        scheduled_start = if_none_replace_with_strnull(self.scheduled_start)
        actual_start = if_none_replace_with_strnull(self.actual_start)
        if scheduled_start != 'NULL':
            scheduled_start = "'" + scheduled_start + "'"
        if actual_start != 'NULL':
            actual_start = "'" + actual_start + "'"
        db.session.execute("""INSERT INTO events (name, slug, active, type, sport, status, scheduled_start, actual_start) 
                              VALUES ('{0}', '{1}', {2}, {3}, 
                              {4}, {5}, {6}, {7})""".format(self.name,
                                                            self.slug,
                                                            self.active,
                                                            self.type,
                                                            self.sport,
                                                            self.status,
                                                            scheduled_start,
                                                            actual_start))
        db.session.commit()
        if self.active:
            SportModel.active_events_check(self.sport)

    def update_in_db(self, slug, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name'][0]
        if 'active' in kwargs:
            self.active = kwargs['active'][0]
        if 'type' in kwargs:
            self.type = EventType.str_to_int(kwargs['type'][0])
        if 'status' in kwargs:
            self.status = EventStatus.str_to_int(kwargs['status'][0])
        if 'scheduled_start' in kwargs:
            self.scheduled_start = kwargs['scheduled_start'][0] #dt.strptime(kwargs['scheduled_start'][0], '%Y-%m-%d %H:%M:%S')
        if 'actual_start' in kwargs:
            self.actual_start = kwargs['actual_start'][0] #dt.strptime(kwargs['actual_start'][0], '%Y-%m-%d %H:%M:%S')

        scheduled_start = if_none_replace_with_strnull(self.scheduled_start)
        actual_start = if_none_replace_with_strnull(self.actual_start)
        if scheduled_start != 'NULL':
            scheduled_start = "'" + self.scheduled_start + "'"
        if actual_start != 'NULL':
            actual_start = "'" + self.actual_start + "'"

        db.session.execute("""UPDATE events 
                              SET name = '{0}', 
                                  active = {1},
                                  type = {2},
                                  status = {3},
                                  scheduled_start = {4},
                                  actual_start = {5} 
                              WHERE slug = '{6}'""".format(self.name,
                                                           self.active,
                                                           self.type,
                                                           self.status,
                                                           scheduled_start,
                                                           actual_start,
                                                           slug))
        db.session.commit()
        SportModel.active_events_check(self.sport)

    @classmethod
    def find_by_params(cls, **kwargs):
        matched_models = []
        event_filter_arr = []
        selection_filter_arr = []
        having_arr = []
        having_str = ''
        event_filter_str = ''
        selection_filter_str = ''

        for key, value in kwargs.items():
            key = str(key).lower()
            val = str(value[0])
            operator = '='
            if val == '':
                key, operator, val = parse_key_val_with_operator(key)
            if 'selection' in key:
                key = 's.' + key.split('selection_')[1]
                if 'count' in key:
                    having_arr.append(parse_clauses_for_query('count(se.id)', operator, val))
                else:
                    selection_filter_arr.append(parse_clauses_for_query(key, operator, val))
            else:
                key = 'e.' + key
                if key == 'e.name' or key == 'e.slug':
                    event_filter_arr.append(parse_clauses_for_query(key, 'REGEXP', val, is_string=True))
                elif 'start' in key:
                    event_filter_arr.append(parse_clauses_for_query(key, operator, val, is_string=True))
                elif key == 'type':
                    event_filter_arr.append(parse_clauses_for_query(key, operator, str(EventType.str_to_int(val))))
                elif key == 'status':
                    event_filter_arr.append(parse_clauses_for_query(key, operator, str(EventStatus.str_to_int(val))))
                else:
                    event_filter_arr.append(parse_clauses_for_query(key, operator, val))

        if len(event_filter_arr) > 0:
            event_filter_str = ' WHERE ' + ' AND '.join(event_filter_arr) + ' '
        if len(selection_filter_arr) > 0:
            selection_filter_str = ' WHERE ' + ' AND '.join(selection_filter_arr) + ' '
        if len(having_arr) > 0:
            having_str = 'HAVING ' + ' AND '.join(having_arr) + ' '

        query = """SELECT DISTINCT
                                    e.id as id,
                                    e.name as name,
                                    e.slug as slug,
                                    e.active as active,
                                    e.type as type,
                                    e.sport as sport,
                                    e.status as status,
                                    e.scheduled_start as scheduled_start,
                                    e.actual_start as actual_start,
                                    count(se.id) as cnt
                           FROM events e
                           LEFT JOIN (
                                SELECT s.id, s.name, s.event, s.active, s.outcome
                                FROM selections s""" + selection_filter_str + \
                """) se
                ON e.id=se.event""" + event_filter_str + """ GROUP BY 1,2,3,4,5,6,7,8,9 """ + having_str

        print(query)
        result = db.session.execute(query)
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

    @classmethod
    def active_selections_check(cls, event_id):
        event = EventModel.find_by_field(event_id, field_name='id')
        event_with_active_selections = EventModel.find_by_params(**{'id': [event_id], 'selection_active': [1]})
        if not event.active and len(event_with_active_selections) > 0:
            event.update_in_db(event.slug, **{'active': [1]})
        elif event.active and len(event_with_active_selections) == 0:
            event.update_in_db(event.slug, **{'active': [0]})
