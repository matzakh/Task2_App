from db import db

from flask import Flask
from flask_restful import Api
from resources.sport import Sport


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():

        db.init_app(app)
        db.create_all()

        @app.route('/')
        def home():
            return 'Success'

        api.add_resource(Sport, '/sport/<string:slug>')

        return app


app = init_app()

if __name__ == '__main__':
    app.run()
