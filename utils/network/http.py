"""
HTTP Communication utility.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""

import requests
import random

from utils.logging.log import Log


class HTTP:
    """HTTP Communication class for request & response from remote HTTP server."""
    @classmethod
    def request(cls, url, tor_network=False, ini=None):
        """Request URL and get response header and body"""
        try:
            if tor_network:
                if not ini:
                    raise ValueError("Config file not found")

                server = '{}://{}:{}'.format(ini.read('TOR', 'PROTOCOL'),
                    ini.read('TOR', 'HOST'),
                    ini.read('TOR', 'PORT'))
                proxies = {'http': server, 'https': server}
                return requests.get(url, proxies=proxies, headers=cls._generate_custom_http_header())
            else:
                return requests.get(url, headers=cls._generate_custom_http_header())
        except Exception as e:
            Log.e("Exception at HTTP.request\n{}".format(e))

    @staticmethod
    def _generate_custom_http_header():
        """"""
        return {
            'User-Agent': random.choice([
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)',
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                'Mozilla/5.0 (Linux; U; Android 4.3; de-de; GT-I9300 Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                'Dalvik/1.6.0 (Linux; U; Android 4.4.4; WT19M-FI Build/KTU84Q)',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
                'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            ])
        }