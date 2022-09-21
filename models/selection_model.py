from db import db
from flask import jsonify
from collections import namedtuple
from enum import IntEnum
from .event_model import EventModel
from common.utils import if_none_replace_with_strnull


class SelectionModel(db.Model):
    __tablename__ = 'selections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    active = db.Column(db.Boolean)
    outcome = db.Column(db.Integer)

    def save_to_db(self):
        pass

    def update_in_db(self, name, **kwargs):
        pass

    @classmethod
    def find_by_params(cls, **kwargs):
        pass

    @classmethod
    def find_by_field(cls, field_value, field_name='name'):
        pass