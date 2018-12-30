from utils.config.ini import Ini
from utils.network.http import HTTP


def test_http():
    response = HTTP().request(
        url='https://www.naver.com',
        tor_network=False
    )

    assert response

    if response:
        assert response.headers


def test_tor_http():
    ini = Ini('files/config.ini')
    response = HTTP().request(
        url='https://facebookcorewwwi.onion',
        tor_network=True,
        ini=ini
    )

    assert response

    if response:
        assert response.headers
