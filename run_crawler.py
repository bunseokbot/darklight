"""
DarkLight Crawler for collect and normalize data from requested url.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""

from crawler import Crawler

from utils.logging.log import Log
from utils.config.ini import Ini

from argparse import ArgumentParser


def main(filepath):
    Log.d("Loading crawler configuration from {} path".format(filepath))
    ini = Ini(filepath)

    # TO-DO: Listen from source


if __name__ == "__main__":
    parser = ArgumentParser(description="DarkLight Crawler")
    parser.add_argument('--config',
                        type=str,
                        dest='config_path',
                        help="Path of crawler configuration file.")

    args = parser.parse_args()
    main(args.config_path)
