from urllib.parse import urlparse

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Domain(Base):
    __tablename__ = 'domains'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(32), unique=True)
    scheme = Column(String(5), nullable=False)
    netloc = Column(String(255), unique=True, nullable=False)

    def __init__(self, uuid, domain):
        parse = urlparse(domain)
        scheme, netloc = parse.scheme, parse.netloc

        # onion domain condition check routine
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
