from pipeline.elastic.documents import Webpage, Service, Port
from pipeline.elastic import Elastic

from pipeline.source.bitcoin import BitcoinPipeline


__all__ = [
    BitcoinPipeline,
]


class Pipeline:
    """Custom pipeline base class for adding custom pipeline."""
    active = True  # Pipeline active status

    def __init__(self, data, ini):
        self.data = data  # DynamicObject type
        self.ini = ini

    def handle(self):
        """Custom pipeline handler."""
        pass

    def __del__(self):
        del self
