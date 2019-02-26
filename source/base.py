"""
Define base class for formatting source collector.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""

from uuid import uuid4

from crawler.tasks import run_crawler

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
                    # add url into database
                    session.add(Domain(uuid=task_id, url=url))
                    session.commit()

                    task = run_crawler.apply_async(args=(url, ), task_id=task_id)
                    Log.i("Crawler issued a new task id {} at {}".format(
                        task.task_id, url))
                except:
                    Log.d("This {} url already saved into database.".format(url))
                finally:
                    self.urls.remove(url)
