"""
Configuration set on local environment class.
"""

import os


class Env:
    @classmethod
    def read(cls, key):
        """Read from local environment variable."""
        return os.environ.get(key, None)

    @classmethod
    def write(cls, key, value):
        """Write to local environment variable."""
        os.environ[key] = value
