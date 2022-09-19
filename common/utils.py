from flask_restful import abort
from models.sport_model import SportModel
from models.event_model import EventModel, EventType, EventStatus
from datetime import datetime as dt


def abort_if_not_exist(item):
    abort(404, message="{} doesn't exist".format(str(item)))


def parse_clauses_for_query(key, operator, value):
    if '|' in value:
        variants = value.split('|')
        return '(' + ' OR '.join([key + ' ' + operator + ' ' + v for v in variants]) + ')'
    else:
        return '(' + key + ' ' + operator + ' ' + value + ')'


def populate_db(sqldb):
    football = SportModel(name='football', slug='football', active=True)
    basketball = SportModel(name='basketball', slug='basketball', active=False)
    sqldb.session.add(football)
    sqldb.session.commit()
    print('football id' + str(football.id))
    sqldb.session.add(basketball)
    sqldb.session.commit()
    print('basketball id' + str(basketball.id))

    football_event1 = EventModel(name='Jupiter vs Saturn',
                                 slug='jupiter_v_saturn',
                                 active=True,
                                 type=EventType.INPLAY,
                                 sport=football.id,
                                 status=EventStatus.PENDING,
                                 scheduled_start=dt.utcnow())

    football_event2 = EventModel(name='Neptune vs Earth',
                                 slug='neptune_v_earth',
                                 active=False,
                                 type=EventType.PREPAY,
                                 sport=football.id,
                                 status=EventStatus.CANCELLED,
                                 scheduled_start=dt.utcnow())

    basketball_event1 = EventModel(name='Andromeda vs Alpha Centauri',
                                 slug='andromeda_v_acentauri',
                                 active=False,
                                 type=EventType.INPLAY,
                                 sport=basketball.id,
                                 status=EventStatus.PENDING,
                                 scheduled_start=dt.utcnow())

    basketball_event2 = EventModel(name='Milky Way Free-for-all',
                                   slug='milkyway_all',
                                   active=False,
                                   type=EventType.PREPAY,
                                   sport=basketball.id,
                                   status=EventStatus.ENDED,
                                   scheduled_start=dt.utcnow())

    sqldb.session.add(football_event1)
    sqldb.session.commit()
    sqldb.session.add(football_event2)
    sqldb.session.commit()
    sqldb.session.add(basketball_event1)
    sqldb.session.commit()
    sqldb.session.add(basketball_event2)
    sqldb.session.commit()
