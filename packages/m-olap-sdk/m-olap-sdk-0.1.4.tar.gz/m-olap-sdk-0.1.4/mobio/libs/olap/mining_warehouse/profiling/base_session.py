from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class BaseSession:
    def __init__(self, olap_uri):
        if not olap_uri:
            raise Exception("OLAP URI is null or empty")
        self.olap_uri = olap_uri
        engine = create_engine(
            url=self.olap_uri, pool_recycle=30
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
