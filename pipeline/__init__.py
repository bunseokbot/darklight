from pipeline.elastic.documents import Webpage, Service, Port
from pipeline.elastic import Elastic


class Pipeline:
    """Custom pipeline base class for adding custom pipeline."""
    active = True  # Pipeline active status

    def __init__(self, uuid, data, ini):
        self.uuid = uuid  # uuid for domain
        self.data = data  # DynamicObject type
        self.ini = ini

    def handle(self):
        """Custom pipeline handler."""
        pass

    def __del__(self):
        del self
