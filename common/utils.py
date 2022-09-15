from flask_restful import abort
from models.sport_model import SportModel


def abort_if_not_exist(item_name):
    abort(404, message="{} doesn't exist".format(item_name))


def populate_db(sqldb):
    football = SportModel(name='football', slug='football', active=True)
    basketball = SportModel(name='basketball', slug='basketball', active=False)
    sqldb.session.add(football)
    sqldb.session.add(basketball)
    sqldb.session.commit()