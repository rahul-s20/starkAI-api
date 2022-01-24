import logging
from sqlalchemy.orm import Session
from app.config.base_class import Base
from sqlalchemy import create_engine
from os import environ as env

logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line

    SQLALCHEMY_DATABASE_URI = env['SQLDBURI']

    engine = create_engine(
        SQLALCHEMY_DATABASE_URI,
        # required for sqlite
        # connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
