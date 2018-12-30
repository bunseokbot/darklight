"""
Socket connection ping checker

Developed by Namjun Kim (bunseokbot@gmail.com)
"""

import socks


class Socket:
    def __init__(self, tor_network=False, ini=None):
        self.tor_network = tor_network
        if self.tor_network and not ini:
            raise ValueError("Config object not found")
        self.ini = ini

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def ping_check(self, address, port):
        """Ping check for check port open."""
        sock = socks.socksocket()
        if self.tor_network:
            sock.setproxy(
                socks.PROXY_TYPE_SOCKS5,
                self.ini.read('TOR', 'HOST'),
                int(self.ini.read('TOR', 'PORT')))

        try:
            sock.connect((address, port))
            sock.close()
            return True
        except:
            return False

    def __del__(self):
        del self
