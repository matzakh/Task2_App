from db import db
import os

from flask import Flask
from flask_restful import Api
from resources.sport import Sport, SportList
from resources.event import Event, EventList
from resources.selection import Selection, SelectionList


def init_app():
    app = Flask(__name__)
    api = Api(app)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test_db.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():

        db.init_app(app)

        @app.route('/')
        def home():
            return 'App started successfully', 200

        api.add_resource(Sport, '/sport/<string:slug>')
        api.add_resource(SportList, '/sport/search')
        api.add_resource(Event, '/event/<string:slug>')
        api.add_resource(EventList, '/event/search')
        api.add_resource(Selection, '/selection/<int:id>')
        api.add_resource(SelectionList, '/selection/search')

        return app


app = init_app()

if __name__ == '__main__':
    app.run()
