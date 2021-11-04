from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.route import router


def create_app():
    app = FastAPI()
    app.include_router(router)
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@localhost/stark_dev'
#     database.init_app(app)
#     app.register_blueprint(blueprint_api)
#     CORS(app, support_credentials=True)
#     return app
