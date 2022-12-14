from flask_restful import request, Resource, abort
from models.event_model import EventModel
from models.sport_model import SportModel
from common.utils import abort_if_not_exist
from marshmallow import Schema, fields, validate


class EventSchema(Schema):
    name = fields.Str(required=False)
    slug = fields.Str(required=False)
    active = fields.Boolean(required=False)
    type = fields.Integer(required=False, validate=validate.OneOf([1, 2]))
    sport = fields.Integer(required=False)
    status = fields.Integer(required=False, validate=validate.OneOf([1, 2, 3, 4]))
    scheduled_start = fields.DateTime(required=False)
    actual_start = fields.DateTime(required=False)


schema = EventSchema()


class Event(Resource):

    def get(self, slug):
        result = EventModel.find_by_field(slug)
        if result is None:
            abort_if_not_exist(slug)
        return result.json()

    def post(self, slug):
        try:
            schema.load(request.form, partial=('scheduled_start', 'actual_start'))
        except:
            abort(400, message="Invalid fields")
        if len(EventModel.find_by_params(**request.form)) > 0:
            abort(400, message="This event already exists")

        sport = SportModel.find_by_field(request.form['sport'], field_name='id')
        if sport is None:
            abort_if_not_exist('Sport ID ' + str(request.form['sport']))

        scheduled_start = None
        actual_start = None
        if 'scheduled_start' in request.form:
            scheduled_start = request.form['scheduled_start']
        if 'actual_start' in request.form:
            actual_start = request.form['actual_start']

        model = EventModel(name=request.form['name'],
                           slug=slug,
                           active=request.form['active'],
                           type=request.form['type'],
                           sport=request.form['sport'],
                           status=request.form['status'],
                           scheduled_start=scheduled_start,
                           actual_start=actual_start)
        model.save_to_db()
        return model.json()

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
        if 'sport' in request.form:
            sport = SportModel.find_by_field(request.form['sport'], field_name='id')
            if sport is None:
                abort_if_not_exist('Sport ID ' + str(request.form['sport']))

        model.update_in_db(slug, **request.form)
        return model.json()


class EventList(Resource):

    def get(self):

        result = EventModel.find_by_params(**request.args)

        if len(result) < 1:
            abort_if_not_exist(request.args)

        return {'events': [i.json().json for i in result]}, 200
