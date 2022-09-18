from flask_restful import request, Resource, abort
from models.event_model import EventModel
from common.utils import abort_if_not_exist
from marshmallow import Schema, fields


class Event(Resource):

    def get(self, slug):
        result = EventModel.find_by_field(slug)
        if result is None:
            abort_if_not_exist(slug)
        return result.json()
