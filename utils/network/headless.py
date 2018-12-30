"""
Headless browser utility

Developed by Namjun Kim (bunseokbot@gmail.com)
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

from urllib.parse import urlparse
from io import BytesIO


class InvalidURLException(Exception):
    # Invalid URL or Website is closed
    pass


class InvalidHTMLException(Exception):
    # Invalid HTML Format
    pass


class BrowserException(Exception):
    # Browser got exception when headless browser return as adnormal
    pass


class HeadlessBrowser:
    """Selenium headless browser for crawling information."""

    def __init__(self, ini, load_image=False, tor_network=False):
        service_args = []
        service_log_path = '/dev/null'

        # if browser don't load image
        if not load_image:
            service_args.append('--load-images=no')

        # selenium connect tor proxy
        if tor_network:
            proxy = '{}:{}'.format(
                ini.read('TOR', 'HOST'),
                ini.read('TOR', 'PORT'))

            service_args.append('--proxy={}'.format(proxy))
            service_args.append('--proxy-type=socks5')

        self.driver = webdriver.PhantomJS(
            executable_path=ini.read('HEADLESS', 'PATH'),
            service_args=service_args,
            service_log_path=service_log_path
        )

    def run(self, url):
        try:
            self.driver.get(url)
        except:
            # browser scan failed
            raise BrowserException

        # if driver source is none
        if not self.get_source():
            raise InvalidURLException

        try:
            # beautifulsoup object for parse html source
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        except:
            # website source code is not HTML
            raise InvalidHTMLException

    def get_sublinks(self):
        """Get all href link from html source."""
        urls = []

        for a in self.soup.find_all('a'):
            try:
                parse = urlparse(a['href'])

                # valid onion domain check routine
                if parse.scheme.startswith('http') and parse.netloc.endswith('onion'):
                    url = "{}://{}".format(parse.scheme, parse.netloc)
                    if url not in urls:
                        urls.append(url)
            except:
                pass

        return urls

    def get_title(self):
        """Get Website title."""
        try:
            return self.soup.title.string
        except:
            return ''

    def get_source(self):
        """Get HTML rendered source."""
        if self.driver.page_source != '<html><head></head><body></body></html>':
            return self.driver.page_source

    def get_lang(self):
        """Get website html language code."""
        return self.soup.html.get('lang', '')

    def get_screenshot(self):
        """Capture browser screenshot with scrolling."""
        element = self.driver.find_element_by_tag_name('body')
        image = Image.open(BytesIO(element.screenshot_as_png)).convert('RGB')

        # crop image when image height is over 30000 (limitation 65500 in JPEG)
        if image.height > 30000:
            image = image.crop((0, 0, image.width, 30000))

        with BytesIO() as f:
            image.save(f, format='jpeg')
            return f.getvalue()

    def __del__(self):
        self.driver.quit()
