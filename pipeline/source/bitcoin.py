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
address_identifier = Table('address_identifier', Base.metadata,
    Column('domain_id', Integer, ForeignKey('domains.id')),
    Column('address_id', Integer, ForeignKey('addresses.id'))
)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address = Column(String(34), unique=True)
    domains = relationship('Domain', secondary=address_identifier)


class BitcoinPipeline(Pipeline):
    name = 'bitcoin'

    def handle(self):
        super(BitcoinPipeline, self).handle()
        addresses = re.findall(
            r'([13][a-km-zA-HJ-NP-Z0-9]{26,33})', self.data.webpage.source)

        engine = Engine.create(ini=self.ini)

        with Session(engine=engine) as session:
            for address in addresses:
                if self.validate_address(address):
                    Log.d("{} address is valid address".format(address))
                    instance = get_or_create(session, Address, address=address)
                    instance.domains.add(self.domain)
                    instance.save()

        engine.dispose()

    def validate_address(self, address):
        """Check validation of address."""
        try:
            timestamp = requests.get(
                'https://blockchain.info/q/addressfirstseen/{}'.format(address),
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0'}).text
            if len(timestamp) == 10:
                return True
        except:
            pass
