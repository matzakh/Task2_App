from flask_restful import request, Resource, abort
from models.sport_model import SportModel
from common.utils import abort_if_not_exist
from marshmallow import Schema, fields


class SportSchema(Schema):
    name = fields.Str(required=False)
    slug = fields.Str(required=False)
    active = fields.Boolean(required=False)


schema = SportSchema()


class Sport(Resource):
    """ post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'name', dest='name',
        location='form', required=False
    )
    post_parser.add_argument(
        'slug', dest='slug',
        location='form',
        required=False
    )
    post_parser.add_argument(
        'active', dest='active',
        type=bool, location='form',
        default=False
    )

    sport_fields = {
        'name': fields.String,
        'slug': fields.String,
        'active': fields.Boolean
    } """

    def get(self, slug):
        result = SportModel.find_by_slug(slug)
        if result is None:
            abort_if_not_exist(slug)
        return result.json()

    # @marshal_with(sport_fields)
    def post(self, slug):
        print(request.form.to_dict())
        try:
            schema.load(request.form)
        except:
            abort(400, message="Invalid fields")

        print(request.form['name'],request.form['slug'],request.form['active'])

        model = SportModel(name=request.form['name'],
                           slug=request.form['slug'],
                           active=request.form['active'])
        print(model)
        model.save_to_db()
        return model.json()

    # @marshal_with(sport_fields)
    def put(self, **kwargs):
        pass

    def delete(self):
        pass


class SportList(Resource):

    def get(self):
        error = schema.validate(request.args)
        if error:
            abort(400, message=str(error))

        result = SportModel.find_by_params(**request.args)

        if len(result) < 1:
            abort_if_not_exist(request.args)

        return {'sports': [i.json().json for i in result]}, 200
