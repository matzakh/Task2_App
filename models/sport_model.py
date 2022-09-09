from db import db
from flask import jsonify


class SportModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String(50))
    active = db.Column(db.Boolean)

    def __init__(self, name, slug, active):
        self.name = name
        self.slug = slug
        self.active = active

    def __repr__(self):
        return "<Sport %s>" % self.name

    def json(self):
        return jsonify({
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'active': self.active
        })

    @classmethod
    def find_by_params(cls, **kwargs):
        pass

    @classmethod
    def find_by_id(cls, q_id):
        pass

