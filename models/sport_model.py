from db import db
from flask import jsonify
from collections import namedtuple


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
        print(kwargs)
        self.name = kwargs['name'][0]
        self.active = kwargs['active'][0]
        db.session.execute('UPDATE sports SET name = "{0}", active = {1} WHERE slug = "{2}"'.format(self.name,
                                                                                                    self.active,
                                                                                                    slug))
        db.session.commit()

    @classmethod
    def find_by_params(cls, **kwargs):
        matched_models = []
        filter_str = ''

        for key, value in kwargs.items():
            val = value[0]
            if key == 'name' or key == 'slug':
                filter_str += str(key) + ' REGEXP "' + str(val) + '" and '
            elif val.lower() == 'true':
                filter_str += str(key) + ' and '
            elif val.lower() == 'false':
                filter_str += 'not ' + str(key) + ' and '
            else:
                filter_str += str(key) + '=' + str(val) + ' and '

        filter_str = filter_str[:-5]

        result = db.session.execute('SELECT * FROM sports WHERE ' + filter_str)
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
        pass
