from database.engine import Engine
from database.session import Session

from pipeline import Pipeline

import re


class BitcoinPipeline(Pipeline):
    name = 'bitcoin'

    def handle(self):
        super(BitcoinPipeline, self).handle()
        addresses = re.findall(
            r'([13][a-km-zA-HJ-NP-Z0-9]{26,33})',
            self.data.webpage.source
        )

        engine = Engine.create(ini=self.ini)

        with Session(engine=engine) as session:
            for address in addresses:
                pass
