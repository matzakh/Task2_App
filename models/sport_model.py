from db import db
from flask import jsonify
from collections import namedtuple


class SportModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean)

    def __init__(self, name, slug, active):
        self.name = name
        self.slug = slug
        self.active = active

    def __repr__(self):
        return "<Sport %r>" % self.name

    def json(self):
        return jsonify({
            'name': self.name,
            'slug': self.slug,
            'active': self.active
        })

    @classmethod
    def find_by_params(cls, **kwargs):
        matched_models = []
        filter_str = ''

        for key, value in kwargs.items():
            filter_str += str(key) + '=' + str(value) + ' and '

        filter_str -= ' and '

        result = db.session.execute('SELECT * FROM sport_model WHERE ' + filter_str)
        Record = namedtuple('Record', result.keys())
        records = [Record(*r) for r in result.fetchall()]

        for r in records:
            matched_models.append(SportModel(name=r.name, slug=r.slug, active=r.active))

        return matched_models

    @classmethod
    def find_by_slug(cls, slug):
        result = db.session.execute('SELECT * FROM sport_model WHERE slug = :val', {'val': slug})
        Record = namedtuple('Record', result.keys())
        records = [Record(*r) for r in result.fetchall()]
        for r in records:
            return SportModel(name=r.name, slug=r.slug, active=r.active)

    @classmethod
    def find_by_id(cls, q_id):
        pass

