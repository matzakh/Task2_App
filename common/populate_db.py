from models.sport_model import SportModel
from models.event_model import EventModel, EventType, EventStatus
from models.selection_model import SelectionModel, SelectionOutcome
from datetime import datetime as dt


def populate_db(sqldb):
    football = SportModel(name='football', slug='football', active=True)
    basketball = SportModel(name='basketball', slug='basketball', active=False)
    sqldb.session.add(football)
    sqldb.session.commit()
    sqldb.session.add(basketball)
    sqldb.session.commit()

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

    event1_selection1 = SelectionModel(name='Event 1 Selection 1', event=1, active=0, outcome=3)
    event1_selection2 = SelectionModel(name='Event 1 Selection 2', event=1, active=1, outcome=1)
    event2_selection2 = SelectionModel(name='Event 2 Selection 1', event=2, active=1, outcome=1)
    event3_selection1 = SelectionModel(name='Event 3 Selection 1', event=3, active=0, outcome=1)

    sqldb.session.add(event1_selection1)
    sqldb.session.commit()
    sqldb.session.add(event1_selection2)
    sqldb.session.commit()
    sqldb.session.add(event2_selection2)
    sqldb.session.commit()
    sqldb.session.add(event3_selection1)
    sqldb.session.commit()
