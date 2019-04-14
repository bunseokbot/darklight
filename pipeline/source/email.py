from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from utils.logging.log import Log

from database.engine import Engine
from database.session import Session
from database.models import Base, get_or_create

from pipeline import Pipeline

import requests
import re


# Database Model for pipeline
email_identifier = Table('email_identifier', Base.metadata,
    Column('domain_id', Integer, ForeignKey('domains.id')),
    Column('email_id', Integer, ForeignKey('emails.id'))
)

class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True)
    email = Column(String(1024), unique=True)
    domains = relationship('Domain', secondary=email_identifier)


class EmailPipeline(Pipeline):
    name = 'email'

    def handle(self):
        super(EmailPipeline, self).handle()
        emails = re.findall(
            r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', self.data.webpage.source)

        engine = Engine.create(ini=self.ini)

        with Session(engine=engine) as session:
            for email in emails:
                instance = get_or_create(session, Email, email=email)
                instance.domains.append(self.domain)
                session.add(instance)
                session.commit()

        engine.dispose()
