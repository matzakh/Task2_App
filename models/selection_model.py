from db import db
from flask import jsonify
from collections import namedtuple
from enum import IntEnum
from .event_model import EventModel
from common.utils import if_none_replace_with_strnull


class SelectionOutcome(IntEnum):
    UNSETTLED = 1
    VOID = 2
    LOSE = 3
    WIN = 4

    @classmethod
    def str_to_int(cls, str_val):
        if not isinstance(str_val, str):
            return str_val
        if str_val.isdigit():
            return int(str_val)
        if str_val.lower() == 'unsettled':
            return cls.UNSETTLED
        elif str_val.lower() == 'void':
            return cls.VOID
        elif str_val.lower() == 'lose':
            return cls.LOSE
        elif str_val.lower() == 'win':
            return cls.WIN
        else:
            return None


class SelectionModel(db.Model):
    __tablename__ = 'selections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    active = db.Column(db.Boolean)
    outcome = db.Column(db.Integer)

    def __init__(self, name, event, active, outcome):
        self.name = name
        if isinstance(event, str):
            if event.isalpha():
                event = EventModel.find_by_field(event, field_name='name').id
            else:
                event = int(event)
        self.event = event
        self.active = active
        self.outcome = SelectionOutcome.str_to_int(outcome)

    def __repr__(self):
        return "<Selection %r>" % self.name

    def _assign_id(self, id):
        self.id = id
        return self

    def json(self):
        return jsonify({
            'id': self.id,
            'name': self.name,
            'event': self.event,
            'active': self.active,
            'outcome': self.outcome
        })

    def save_to_db(self):
        db.session.execute("""INSERT INTO selections (name, event, active, outcome) 
                              VALUES ('{0}', {1}, {2}, {3})""".format(self.name,
                                                                      self.event,
                                                                      self.active,
                                                                      self.outcome))
        db.session.commit()
        # check for active for events

    def update_in_db(self, id, **kwargs):
        pass

    @classmethod
    def find_by_params(cls, **kwargs):
        pass

    @classmethod
    def find_by_field(cls, field_value, field_name='id'):
        if field_name == 'outcome':
            field_value = SelectionOutcome.str_to_int(field_value)
        if isinstance(field_value, str):
            field_value = '"' + field_value + '"'
        result = db.session.execute('SELECT * FROM selections WHERE {0} = {1} LIMIT 1'.format(field_name, field_value))
        Record = namedtuple('Record', result.keys())
        records = [Record(*r) for r in result.fetchall()]
        for r in records:
            return SelectionModel(name=r.name,
                                  event=r.event,
                                  active=r.active,
                                  outcome=r.outcome)._assign_id(r.id)