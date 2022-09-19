from flask_restful import request, Resource, abort
from models.event_model import EventModel
from common.utils import abort_if_not_exist
from marshmallow import Schema, fields


class EventSchema(Schema):
    name = fields.Str(required=False)
    slug = fields.Str(required=False)
    active = fields.Boolean(required=False)
    type = fields.Integer(required=False)
    sport = fields.Integer(required=False)
    status = fields.Integer(required=False)
    scheduled_start = fields.Integer(required=False)
    actual_start = fields.Integer(required=False)


schema = EventSchema()


class Event(Resource):

    def get(self, slug):
        result = EventModel.find_by_field(slug)
        if result is None:
            abort_if_not_exist(slug)
        return result.json()


class EventList(Resource):

    def get(self):
        error = schema.validate(request.args)
        if error:
            abort(400, message=str(error))

        result = EventModel.find_by_params(**request.args)

        if len(result) < 1:
            abort_if_not_exist(request.args)

        return {'events': [i.json().json for i in result]}, 200
