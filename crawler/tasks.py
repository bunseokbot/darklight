from utils.logging.log import Log
from utils.config.ini import Ini
from utils.config.env import Env

from . import Crawler
from .celery import app


@app.task(bind=True)
def run_crawler(self, url):
    Log.i(f"Starting crawler task for {url}")

    crawler = Crawler(ini=Ini(Env.read("CONFIG_FILE")))

    report = crawler.scan(url)

    if not report.is_empty() and report.webpage.url == url:
        crawler.save(self.request.id, report)

    del crawler
