from db import db
from flask import jsonify
from collections import namedtuple
from common.utils import parse_clauses_for_query, parse_key_val_with_operator


class SportModel(db.Model):
    __tablename__ = 'sports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean)

    def __init__(self, name, slug, active):
        self.name = name
        self.slug = slug
        self.active = active

    def _assign_id(self, id):
        self.id = id
        return self

    def __repr__(self):
        return "<Sport %r>" % self.name

    def json(self):
        return jsonify({
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'active': self.active
        })

    def save_to_db(self):
        db.session.execute('INSERT INTO sports (name, slug, active) VALUES ("{0}", "{1}", {2})'.format(self.name,
                                                                                                       self.slug,
                                                                                                       self.active))
        db.session.commit()

    def delete_from_db(self):
        db.session.execute('DELETE FROM sports WHERE ("{0}", "{1}", {2})'.format(self.name,
                                                                                 self.slug,
                                                                                 self.active))
        db.session.commit()

    def update_in_db(self, slug, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name'][0]
        if 'active' in kwargs:
            self.active = kwargs['active'][0]
        db.session.execute('UPDATE sports SET name = "{0}", active = {1} WHERE slug = "{2}"'.format(self.name,
                                                                                                    self.active,
                                                                                                    slug))
        db.session.commit()

    @classmethod
    def find_by_params(cls, **kwargs):
        matched_models = []
        sport_filter_arr = []
        event_filter_arr = []
        having_arr = []
        having_str = ''
        sport_filter_str = ''
        event_filter_str = ''

        for key, value in kwargs.items():
            key = str(key).lower()
            val = str(value[0])
            operator = '='
            if val == '':
                key, operator, val = parse_key_val_with_operator(key)
            if 'event' in key:
                key = 'e.' + key.split('event_')[1]
                if 'count' in key:
                    having_arr.append(parse_clauses_for_query('count(ev.id)', operator, val))
                else:
                    event_filter_arr.append(parse_clauses_for_query(key, operator, val))
            else:
                key = 's.' + key
                if key == 's.name' or key == 's.slug':
                    sport_filter_arr.append(parse_clauses_for_query(key, 'REGEXP', val, is_string=True))
                else:
                    sport_filter_arr.append(parse_clauses_for_query(key, operator, val))

        if len(sport_filter_arr) > 0:
            sport_filter_str = ' WHERE ' + ' AND '.join(sport_filter_arr) + ' '
        if len(event_filter_arr) > 0:
            event_filter_str = ' WHERE ' + ' AND '.join(event_filter_arr) + ' '
        if len(having_arr) > 0:
            having_str = 'HAVING ' + ' AND '.join(having_arr) + ' '

        query = """SELECT DISTINCT
                            s.id as id,
                            s.name as name,
                            s.slug as slug,
                            s.active as active,
                            count(ev.id) as cnt
                   FROM sports s 
                   LEFT JOIN (
                        SELECT e.id, e.sport, e.name, e.slug, e.active, 
                               e.scheduled_start, e.actual_start, e.status, e.type
                        FROM events e""" + event_filter_str + \
                   """) ev 
                   ON s.id=ev.sport""" + sport_filter_str + """ GROUP BY 1,2,3,4 """ + having_str

        print(query)
        result = db.session.execute(query)
        Record = namedtuple('Record', result.keys())
        records = [Record(*r) for r in result.fetchall()]

        for r in records:
            matched_models.append(SportModel(name=r.name, slug=r.slug, active=r.active)._assign_id(r.id))

        return matched_models

    @classmethod
    def find_by_field(cls, field_value, field_name='slug'):
        if isinstance(field_value, str):
            field_value = '"' + field_value + '"'
        result = db.session.execute('SELECT * FROM sports WHERE {0} = {1} LIMIT 1'.format(field_name, field_value))
        Record = namedtuple('Record', result.keys())
        records = [Record(*r) for r in result.fetchall()]
        for r in records:
            return SportModel(name=r.name, slug=r.slug, active=r.active)._assign_id(r.id)

    @classmethod
    def active_events_check(cls, sport_id):
        sport = SportModel.find_by_field(sport_id, field_name='id')
        sport_with_active_events = SportModel.find_by_params(**{'id': [sport.id], 'event_active': [1]})
        if not sport.active and len(sport_with_active_events) > 0:
            sport.update_in_db(sport.slug, **{'name': [sport.name], 'active': [1]})
        elif sport.active and len(sport_with_active_events) == 0:
            sport.update_in_db(sport.slug, **{'name': [sport.name], 'active': [0]})

