from flask import Flask
from db import db
from api import api
from cron import cron
from charts import init_dash


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('app.cfg', True)

    db.init_app(app)
    api.init_app(app)
    cron.init_app(app)

    with app.app_context():
        from routes import routes
        app.register_blueprint(routes)

        init_dash(app)

        db.create_all()

        cron.start()

        return app
