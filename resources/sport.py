from flask_restful import fields, marshal_with, reqparse, Resource
from models.sport_model import SportModel
from common.utils import abort_if_not_exist
from marshmallow import Schema, fields


class SportSchema(Schema):
    name = fields.Str(required=False)
    slug = fields.Str(required=False)
    active = fields.Boolean(required=False)


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
    def post(self, **kwargs):
        pass

    # @marshal_with(sport_fields)
    def put(self, **kwargs):
        pass

    def delete(self):
        pass


class SportList(Resource):

    def get(self, **kwargs):
        pass
