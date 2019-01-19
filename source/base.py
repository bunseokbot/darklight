"""
Define base class for formatting source collector.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""

from uuid import uuid4

from crawler.tasks import CrawlerTask

from database.session import Session
from database.engine import Engine
from database.models import Domain

from utils.logging.log import Log
from utils.config.ini import Ini
from utils.config.env import Env


class SourceBase(object):
    """Base source object class format."""
    urls = []
    ini = Ini(Env.read('CONFIG_FILE'))
    active = True  # collector status

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
        engine = Engine.create(self.ini)
        with Session(engine=engine) as session:
            for url in self.urls:
                task_id = uuid4().hex

                try:
                    session.add(Domain(task_id, url))
                    task = CrawlerTask().apply_async(args=[url], task_id=task_id)
                    Log.i("CrawlerTask issued a new task id: {}".format(task.task_id))
                except:
                    Log.d("This {} url already saved into database.".format(url))
                finally:
                    self.urls.remove(url)

            session.commit()
