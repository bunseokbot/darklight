"""
Ini configuration file class.
"""
from configparser import ConfigParser


class Ini:
    def __init__(self, filename):
        self.config = ConfigParser()
        self.config.read(filename)

    def read(self, title, key):
        """Read value from config file."""
        try:
            return self.config[title][key]
        except:
            return None
