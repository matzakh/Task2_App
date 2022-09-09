from flask_restful import fields, marshal_with, reqparse, Resource
from models.sport_model import SportModel


class Sport(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'name', dest='name',
        location='form', required=True
    )
    post_parser.add_argument(
        'slug', dest='slug',
        location='form',
        required=True
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
    }

    @marshal_with(sport_fields)
    def get(self, **kwargs):
        return SportModel(name=kwargs.name, slug=kwargs.slug, active=kwargs.active)

    @marshal_with(sport_fields)
    def post(self):
        pass

    def delete(self):
        pass