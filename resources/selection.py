from flask_restful import request, Resource, abort
from models.selection_model import SelectionModel
from common.utils import abort_if_not_exist
from marshmallow import Schema, fields


class SelectionSchema(Schema):
    name = fields.Str(required=False)
    event = fields.Integer(required=False)
    active = fields.Boolean(required=False)
    outcome = fields.Integer(required=False)


schema = SelectionSchema()


class Selection(Resource):

    def get(self, id):
        result = SelectionModel.find_by_field(id)
        if result is None:
            abort_if_not_exist(id)
        return result.json()

    def post(self, name):
        try:
            schema.load(request.form)
        except:
            abort(400, message="Invalid fields")
        if len(SelectionModel.find_by_params(**request.form)) > 0:
            abort(400, message="This event already exists")

        model = SelectionModel(name=name,
                               event=request.form['event'],
                               active=request.form['active'],
                               outcome=request.form['outcome'])
        model.save_to_db()
        return model.json()

    def put(self, id):
        try:
            schema.load(request.form)
        except:
            abort(400, message="Invalid fields")
        model = SelectionModel.find_by_field(id)
        if model is None:
            abort_if_not_exist(id)

        model.update_in_db(id, **request.form)
        return model.json()


class SelectionList(Resource):

    def get(self):
        result = SelectionModel.find_by_params(**request.args)

        if len(result) < 1:
            abort_if_not_exist(request.args)

        return {'events': [i.json().json for i in result]}, 200
