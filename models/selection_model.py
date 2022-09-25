from db import db
from flask import jsonify
from collections import namedtuple
from enum import IntEnum
from .event_model import EventModel
from common.utils import if_none_replace_with_strnull, parse_clauses_for_query, parse_key_val_with_operator


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
        EventModel.active_selections_check(self.event)

    def update_in_db(self, id, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name'][0]
        if 'event' in kwargs:
            self.event = kwargs['event'][0]
        if 'active' in kwargs:
            self.active = kwargs['active'][0]
        if 'outcome' in kwargs:
            self.outcome = kwargs['outcome'][0]
        db.session.execute("""UPDATE selections SET name = '{0}', 
                                                    event = {1},
                                                    active = {2},
                                                    outcome = {3}
                              WHERE id = {4}""".format(self.name, self.event, self.active, self.outcome, id))
        db.session.commit()
        EventModel.active_selections_check(self.event)

    @classmethod
    def find_by_params(cls, **kwargs):
        matched_models = []
        selection_filter_arr = []
        selection_filter_str = ''

        for key, value in kwargs.items():
            key = str(key).lower()
            val = str(value[0])
            operator = '='
            if val == '':
                key, operator, val = parse_key_val_with_operator(key)
            else:
                key = 's.' + key
                if key == 's.name':
                    selection_filter_arr.append(parse_clauses_for_query(key, 'REGEXP', val, is_string=True))
                elif 'outcome' in key:
                    selection_filter_arr.append(parse_clauses_for_query(key, operator, SelectionOutcome.str_to_int(val)))
                else:
                    selection_filter_arr.append(parse_clauses_for_query(key, operator, val))

        if len(selection_filter_arr) > 0:
            selection_filter_str = ' WHERE ' + ' AND '.join(selection_filter_arr) + ' '

        query = """SELECT DISTINCT
                                    s.id as id,
                                    s.name as name,
                                    s.event as event,
                                    s.active as active,
                                    s.outcome as outcome
                           FROM selections s""" + selection_filter_str

        result = db.session.execute(query)
        Record = namedtuple('Record', result.keys())
        records = [Record(*r) for r in result.fetchall()]

        for r in records:
            matched_models.append(SelectionModel(name=r.name, event=r.event,
                                                 active=r.active, outcome=r.outcome)._assign_id(r.id))

        return matched_models

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

