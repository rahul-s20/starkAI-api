from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.base_class import Base

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456789@localhost/stark_dev'

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    # required for sqlite
    # connect_args={"check_same_thread": False},
)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
