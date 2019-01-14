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


class Webpage(Base):
    __tablename__ = 'webpages'

    id = Column(Integer, primary_key=True)
    scanned_time = Column(DateTime)
    domain_id = Column(Integer, ForeignKey('domains.id'))
    domain = relationship('Domain', backref=backref('Webpage', order_by=id))
    title = Column(String(255), nullable=True)
    language = Column(String(10), nullable=True)
    server = Column(String(255), nullable=True)
    screenshot = Column(Text, nullable=False)


class Port(Base):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True)
    webpage_id = Column(Integer, ForeignKey('webpages.id'))
    webpage = relationship('Webpage', backref=backref('Port', order_by=id))
    scanned_info = Column(Text, nullable=False)
