from urllib.parse import urlparse

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Domain(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(32), unique=True)
    scheme = Column(String(5), nullable=False)
    netloc = Column(String(255), unique=True, nullable=False)

    def __init__(self, uuid, url):
        # onion domain condition check routine
        parse = urlparse(url)
        scheme, netloc = parse.scheme, parse.netloc

        if not netloc.endswith('.onion'):
            raise ValueError("Invalid onion domain")

        self.uuid = uuid
        self.scheme = scheme
        self.netloc = netloc

    def __repr__(self):
        return "<Domain('{}', '{}', '{}')>".format(
            self.uuid, self.scheme, self.netloc
        )


def get_or_create(session, model, **kwargs):
    """Get instance or if not exist, create a new instance."""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
