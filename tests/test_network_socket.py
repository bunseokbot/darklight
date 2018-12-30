from utils.config.ini import Ini
from utils.network.socket import Socket


def test_ping_check():
    with Socket() as socket:
        is_opened = socket.ping_check('darklight.kr', 80)
        assert is_opened == True

        is_closed = socket.ping_check('darklight.kr', 31337)
        assert is_closed == False


def test_tor_ping_check():
    ini = Ini('files/config.ini')
    with Socket(tor_network=True, ini=ini) as socket:
        is_opened = socket.ping_check('facebookcorewwwi.onion', 80)
        assert is_opened == True

        is_closed = socket.ping_check('facebookcorewwwi.onion', 31337)
        assert is_closed == False