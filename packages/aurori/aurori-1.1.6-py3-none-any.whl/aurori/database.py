import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

class SQLAlchemy(object):
    """
    """

    def __init__(self, ):
        self.engine = None
        self.url = ""
        self.sessionmaker = None

    def init_app(self, config):
        if "database_path" in config["SYSTEM"] and config["SYSTEM"]["database_path"] != "":
            self.url = "sqlite:///" + config["SYSTEM"]["database_path"]
        else:
            logging.warning("Using fallback database url")
            self.url = "sqlite:///./sqlite3.db"

        self.engine = create_engine(
            self.url, connect_args={"check_same_thread": False}
        )
        self.sessionmaker = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))

    @contextmanager
    def get_session(self):
        db_session = (self.sessionmaker)()
        try:
            yield db_session
        finally:
            db_session.close()

db = SQLAlchemy()

SQLModelBase = declarative_base()
