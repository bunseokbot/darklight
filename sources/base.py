"""
Define base class for formatting source collector.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""

from crawler.tasks import CrawlerTask
from utils.logging.log import Log


class SourceBase(object):
    """Base source object class format."""
    urls = []

    def collect(self):
        """
        Run user custom method.
        :return:
        """
        pass

    def save(self):
        """
        Save domain on database and request crawling.
        :return: None
        """
        for url in self.urls:
            task = CrawlerTask.delay(url=url)
            Log.i("CrawlerTask issued a new task id: {}".format(task.task_id))
            self.urls.remove(url)
