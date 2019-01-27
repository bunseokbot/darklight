from utils.network.headless import (
    HeadlessBrowser, InvalidHTMLException, InvalidURLException
)
from utils.network.socket import Socket
from utils.logging.log import Log
from utils.type.dynamic import DynamicObject

from database.session import Session
from database.engine import Engine
from database.models import Domain

from pipeline.elastic import Elastic
from pipeline.elastic.documents import Webpage, Service, Port

from urllib.parse import urlparse

import pipeline.source as pipelines


class Crawler:
    """
    DarkLight onion domain crawler.
    """
    def __init__(self, ini):
        Log.i("Starting crawler")
        self.ini = ini

    def scan(self, url):
        """Scan and crawl url which user requested."""
        Log.i("Trying to crawl {} url".format(url))

        browser = HeadlessBrowser(
            ini=self.ini,
            tor_network=True
        )

        domain = urlparse(url).netloc
        obj = DynamicObject()

        try:
            # Step 1. Visit website using headless tor browser
            Log.d("Step 1. Visiting {} website using headless browser".format(url))
            obj.webpage = browser.run(url)

            # Step 2. Scan common service port
            Log.d("Step 2. Scanning {} domain's common service port".format(domain))
            obj.port = self._portscan(domain)

            # Step 3. TO-DO

        except InvalidHTMLException:
            Log.e("Invalid HTML returned from website")

        except InvalidURLException:
            Log.e("Invalid URL or website is down")

        finally:
            del browser

        return obj

    def _portscan(self, domain):
        """Scan and check opened port."""
        socket = Socket(
            tor_network=True,
            ini=self.ini,
        )

        # common service port list
        services = [
            {'number': 20, 'status': False},
            {'number': 21, 'status': False},
            {'number': 22, 'status': False},
            {'number': 23, 'status': False},
            {'number': 25, 'status': False},
            {'number': 80, 'status': False},
            {'number': 110, 'status': False},
            {'number': 123, 'status': False},  # NTP
            {'number': 143, 'status': False},
            {'number': 194, 'status': False},  # IRC
            {'number': 389, 'status': False},
            {'number': 443, 'status': False},
            {'number': 993, 'status': False},  # IMAPS
            {'number': 3306, 'status': False},
            {'number': 3389, 'status': False},
            {'number': 5222, 'status': False}, # XMPP
            {'number': 6667, 'status': False}, # Public IRC
            {'number': 8060, 'status': False}, # OnionCat
            {'number': 8333, 'status': False}, # Bitcoin
        ]

        for i in range(len(services)):
            opened = socket.ping_check(domain, services[i]['number'])
            services[i]['status'] = opened
            Log.d("{} port is {}".format(
                services[i]['number'], 'opened' if opened else 'closed'
            ))

        del socket

        return services

    def save(self, id, obj):
        """Save crawled data into database."""
        Log.i("Saving crawled data")

        meta = {
            'id': id,
        }

        engine = Engine.create(ini=self.ini)

        with Session(engine=engine) as session:
            domain = session.query(Domain).filter_by(uuid=id).first()

        engine.dispose()

        # pass the pipeline before saving data (for preprocessing)
        for pipeline in pipelines.__all__:
            _class = pipeline(domain, data=obj, ini=self.ini)

            if _class.active:
                Log.d("handling the {} pipeline".format(_class.name))
                _class.handle()
            else:
                Log.d("{} pipeline isn't active".format(_class.name))

            del _class

        with Elastic(ini=self.ini):
            # upload screenshot at Amazon S3
            screenshot = 'https://darklight.amazon.com/s3/bucket/filename.png'

            Webpage(
                meta=meta,
                url=obj.webpage.url,
                domain=obj.webpage.domain,
                title=obj.webpage.title,
                source=obj.webpage.source,
                screenshot=screenshot,
                language=obj.webpage.language,
                headers=obj.webpage.headers,
            ).save()

            Port(
                meta=meta,
                services=[
                    Service(number=port['number'], status=port['status']) for port in obj.port]
            ).save()

    def __del__(self):
        Log.i("Ending crawler")
        del self
