from utils.config.ini import Ini
from utils.network.headless import HeadlessBrowser
from utils.network.headless import InvalidURLException, InvalidHTMLException

import pytest


ini = Ini('files/config.ini')


def test_browser():
    """Test for running headless browser."""
    browser = HeadlessBrowser(ini=ini)
    browser.run(url='https://www.naver.com')

    screenshot = browser.get_screenshot()
    assert screenshot

    del browser


def test_tor_browser():
    """Test for running headless browser with tor proxy."""
    browser = HeadlessBrowser(
        ini=ini,
        tor_network=True
    )

    browser.run(url='http://wikitjerrta4qgz4.onion')

    screenshot = browser.get_screenshot()
    assert screenshot

    links = browser.get_sublinks()
    assert links

    del browser


def test_invalid_link():
    """Test for invalid link handling."""
    browser = HeadlessBrowser(ini=ini)

    with pytest.raises(InvalidURLException) as e_info:
        browser.run(url='https://test.namjun.kim')

    del browser
