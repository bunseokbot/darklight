from utils.network.headless import (
    HeadlessBrowser, InvalidHTMLException, InvalidURLException
)
from utils.network.socket import Socket
from utils.logging.log import Log
from utils.type.dynamic import DynamicObject

from pipeline import Pipeline

from urllib.parse import urlparse


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

        with Pipeline(id=id, obj=obj, ini=self.ini) as pipeline:
            pipeline.save()

    def __del__(self):
        Log.i("Ending crawler")
        del self
