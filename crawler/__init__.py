from utils.network.headless import (
    HeadlessBrowser, InvalidHTMLException, InvalidURLException
)
from utils.network.socket import Socket
from utils.logging.log import Log
from utils.type.dynamic import DynamicObject

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
            obj = browser.run(url)

            # Step 2. Scan common service port
            Log.d("Step 2. Scanning {} domain's common service port".format(domain))
            obj.ports = self._portscan(domain)

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
        services = {
            20: False,
            21: False,
            22: False,
            23: False,
            25: False,
            80: False,
            110: False,
            123: False,   # NTP
            143: False,
            194: False,   # IRC
            389: False,
            443: False,
            993: False,   # IMAPS
            3306: False,
            3389: False,
            5222: False,  # XMPP
            6667: False,  # Public IRC
            8060: False,  # OnionCat
            8333: False,  # Bitcoin
        }

        for key in services.keys():
            opened = socket.ping_check(domain, key)
            services[key] = opened
            Log.d("{} port is {}".format(
                key, 'opened' if opened else 'closed'
            ))

        del socket

        return services

    def save(self, obj):
        """Save crawled data into database."""
        Log.i("Saving crawled data")

    def __del__(self):
        Log.i("Ending crawler")
        del self
