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

    def put(self, slug):
        try:
            schema.load(request.form, partial=('name','slug','active',
                                               'type','sport','status',
                                               'scheduled_start','actual_start'))
        except:
            abort(400, message="Invalid fields")
        model = EventModel.find_by_field(slug)
        if model is None:
            abort_if_not_exist(slug)

        model.update_in_db(slug, **request.form)
        return model.json()


class EventList(Resource):

    def get(self):
        error = schema.validate(request.args)
        if error:
            abort(400, message=str(error))

        result = EventModel.find_by_params(**request.args)

        if len(result) < 1:
            abort_if_not_exist(request.args)

        return {'events': [i.json().json for i in result]}, 200
