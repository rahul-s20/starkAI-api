from flask import Flask
from flask_cors import CORS
from app.routes.route import blueprint_api
from app.models.modalone import database


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/stark_dev'
    database.init_app(app)
    app.register_blueprint(blueprint_api)
    CORS(app, support_credentials=True)
    return app