from crawler import Crawler

from utils.config.ini import Ini
from utils.type.dynamic import DynamicObject


def test_load_crawler():
    ini = Ini('files/config.ini')
    crawler = Crawler(ini)
    assert crawler

    report = crawler.scan('http://wikitjerrta4qgz4.onion')
    assert type(report) == DynamicObject
    assert report.webpage.url == 'http://wikitjerrta4qgz4.onion'
    assert report.webpage.domain == 'wikitjerrta4qgz4.onion'

    del crawler
