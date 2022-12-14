from flask_restful import request, Resource, abort
from models.sport_model import SportModel
from common.utils import abort_if_not_exist
from marshmallow import Schema, fields


class SportSchema(Schema):
    name = fields.Str(required=False)
    slug = fields.Str(required=False)
    active = fields.Boolean(required=False)
    event_active = fields.Boolean(required=False)


schema = SportSchema()


class Sport(Resource):

    def get(self, slug):
        result = SportModel.find_by_field(slug)
        if result is None:
            abort_if_not_exist(slug)
        return result.json()

    def post(self, slug):
        try:
            schema.load(request.form)
        except:
            abort(400, message="Invalid fields")
        if len(SportModel.find_by_params(**request.form)) > 0:
            abort(400, message="This sport already exists")

        model = SportModel(name=request.form['name'],
                           slug=request.form['slug'],
                           active=request.form['active'])
        model.save_to_db()
        return model.json()

    def put(self, slug):
        try:
            schema.load(request.form, partial=('name', 'slug', 'active'))
        except:
            abort(400, message="Invalid fields")
        model = SportModel.find_by_field(slug)
        if model is None:
            abort_if_not_exist(slug)

        model.update_in_db(slug, **request.form)

        return model.json()

    def delete(self):
        pass


class SportList(Resource):

    def get(self):

        result = SportModel.find_by_params(**request.args)

        if len(result) < 1:
            abort_if_not_exist('This query result')

        return {'sports': [i.json().json for i in result]}, 200
