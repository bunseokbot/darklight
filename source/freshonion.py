from urllib.parse import urlparse

from .base import SourceBase

from utils.logging.log import Log
from utils.network.http import HTTP


class FreshOnionCollector(SourceBase):
    cycle = 10  # minute
    name = 'freshonion'  # collector name
    active = False  # collector status

    def _get_formed_url(self, row):
        parse = urlparse(row['url'])
        return "{}://{}".format(parse.scheme, parse.netloc)

    def collect(self):
        Log.d("Start collecting from freshonion API")
        response = HTTP.request(
            url='http://zlal32teyptf4tvi.onion/json/all',
            tor_network=True,
            ini=self.ini
        )

        if not response:
            Log.e("Exception accrued while loading website.")
            return

        if response.status_code == 200:
            rows = response.json()
            Log.i("{} url detected from freshonion".format(len(rows)))

            for row in rows:
                url = self._get_formed_url(row)
                if url not in self.urls:
                    self.urls.append(url)
