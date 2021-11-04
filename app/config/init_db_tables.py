# import logging
# from sqlalchemy.orm import Session
# from app.config.base import STARKBase
# from app.models.keyModel import Keys
#
# from app.models.keyModel import Keys
# from app.schema.keySchema import Keyssc
# # from app.db import base  # noqa: F401
#
# logger = logging.getLogger(__name__)
#
# FIRST_SUPERUSER = "admin20@stark.com"
#
# # make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# # otherwise, SQL Alchemy might fail to initialize relationships properly
# # for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
#
#
# def init_db(db: Session) -> None:
#     # Tables should be created with Alembic migrations
#     # But if you don't want to use migrations, create
#     # the tables un-commenting the next line
#     # Base.metadata.create_all(bind=engine)
#     key = STARKBase(Keys)
#     if FIRST_SUPERUSER:
#         user = key.get_user_by_email(db, email=FIRST_SUPERUSER)
#         if not user:
#             key_in = Keyssc(
#                 api_key="testw",
#                 email=FIRST_SUPERUSER,
#             )
#             user = key.create(db, obj_in=key_in)  # noqa: F841
#         else:
#             logger.warning(
#                 "Skipping creating superuser. User with email "
#                 f"{FIRST_SUPERUSER} already exists. "
#             )
#     else:
#         logger.warning(
#             "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
#             "provided as an env variable. "
#             "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
#         )