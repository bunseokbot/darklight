from pipeline.elastic.documents import Webpage, Service, Port
from pipeline.elastic import Elastic


class Pipeline:
    """Pipeline class for adding additional data from original source."""

    def __init__(self, id, obj, ini):
        self.id = id
        self.object = obj
        self.ini = ini

    def __enter__(self):
        with Elastic(ini=self.ini) as connection:
            self.connection = connection

        return self


    def save(self):
        meta = {
            'id': self.id
        }

        # upload screenshot at Amazon S3
        screenshot = 'https://darklight.amazon.com/s3/bucket/filename.png'

        Webpage(
            meta=meta,
            url=self.object.webpage.url,
            domain=self.object.webpage.domain,
            title=self.object.webpage.title,
            source=self.object.webpage.source,
            screenshot=screenshot,
            language=self.object.webpage.language,
        ).save(using=self.connection)

        Port(
            meta=meta,
            services=[
                Service(number=port['number'], status=port['status']) for port in self.object.port]
        ).save(using=self.connection)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        del self
