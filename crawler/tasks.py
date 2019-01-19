from celery import Task

from utils.logging.log import Log
from utils.config.ini import Ini
from utils.config.env import Env

from . import Crawler
from .celery import app


class CrawlerTask(Task):
    name = "crawler"

    def __init__(self):
        super(Task, self).__init__()
        Log.i("Starting crawler task")

        self.crawler = Crawler(
            ini=Ini(Env.read('CONFIG_FILE')))

    def run(self, url):
        """Run crawler task and get result."""
        Log.d("Receive {} url from endpoint".format(url))
        report = self.crawler.scan(url)
        self.crawler.save(report)


# register task into app
app.register_task(CrawlerTask())
