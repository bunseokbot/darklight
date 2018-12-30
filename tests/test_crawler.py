from crawler import Crawler

from utils.config.ini import Ini


def test_load_crawler():
    ini = Ini('files/config.ini')
    crawler = Crawler(ini)
    assert crawler
    del crawler
