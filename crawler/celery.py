"""
Celery application.
"""
from utils.config.ini import Ini
from utils.config.env import Env

from celery import Celery


ini = Ini(Env.read('CONFIG_FILE'))

# load celery app
app = Celery(
    'crawler_tasks',
    broker=ini.read('CELERY', 'BROKER_URL'),
    backend=ini.read('CELERY', 'RESULT_BACKEND'))
