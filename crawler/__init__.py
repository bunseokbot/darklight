from utils.network.headless import HeadlessBrowser
from utils.network.headless import InvalidHTMLException, InvalidURLException
from utils.logging.log import Log


class Crawler(object):
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

        try:
            browser.run(url)

            result = {
                'url': url,
                'title': browser.get_title(),
                'screenshot': browser.get_screenshot(),
                'language': browser.get_lang(),
                'source': browser.get_source(),
                'sublinks': browser.get_sublinks()
            }

        except InvalidHTMLException:
            Log.e("Invalid HTML returned from website")

        except InvalidURLException:
            Log.e("Invalid URL or website is down")

        finally:
            del browser

        return result


    def save(self):
        """Save crawled data into database."""
        Log.i("Saving crawled data")

    def __del__(self):
        Log.i("Ending crawler")
        del self
