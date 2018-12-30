import os

from utils.config.ini import Ini


def test_read_ini_file():
    """Test for reading ini file and parse key."""
    ini = Ini(os.path.join('files', 'config.ini'))

    # compare binary path
    binary_path = ini.read('HEADLESS', 'PATH')
    assert \
        binary_path == '/Users/bunseokbot/Documents/darklight_engine/tests/files/phantomjs'

    # compare elasticsearch host
    es_host = ini.read('ELASTICSEARCH', 'HOST')
    assert es_host == '1.1.1.1'
