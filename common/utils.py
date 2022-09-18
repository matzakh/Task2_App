from flask_restful import abort
from models.sport_model import SportModel


def abort_if_not_exist(item):
    abort(404, message="{} doesn't exist".format(str(item)))


def populate_db(sqldb):
    football = SportModel(name='football', slug='football', active=True)
    basketball = SportModel(name='basketball', slug='basketball', active=False)
    sqldb.session.add(football)
    sqldb.session.commit()
    print('football id' + str(football.id))
    sqldb.session.add(basketball)
    sqldb.session.commit()
    print('basketball id' + str(basketball.id))