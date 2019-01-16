"""
Test crawler worker
Celery worker testing code.
"""

from crawler.tasks import CrawlerTask

from mock import patch


def test_start_task():
    with patch('crawler.tasks.CrawlerTask') as mock_task:
        assert mock_task


def test_task_request():
    with patch('crawler.tasks.CrawlerTask'):
        task = CrawlerTask()
        task.run(url='https://facebookcorewwwi.onion')
        """
        task_id = uuid4().hex
        result = task.apply_async(
            args='https://facebookcorewwwi.onion',
            task_id=task_id)
        """

