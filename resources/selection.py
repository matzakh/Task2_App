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


class Selection:

    def get(self, name):
        result = SelectionModel.find_by_field(name)
        if result is None:
            abort_if_not_exist(name)
        return result.json()

    def post(self, name):
        try:
            schema.load(request.form, partial=('outcome'))
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

    def put(self, name):
        try:
            schema.load(request.form, partial=('outcome'))
        except:
            abort(400, message="Invalid fields")
        model = SelectionModel.find_by_field(name)
        if model is None:
            abort_if_not_exist(name)

        model.update_in_db(name, **request.form)
        return model.json()