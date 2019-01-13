"""
Run all sources to collect domain from registered sources.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""
from utils.logging.log import Log

import sources


def main():
    """Main method for running all sources."""
    Log.i("{} source(s) detected!".format(len(sources.__all__)))

    for source in sources.__all__:
        _class = source()
        Log.i("Trying to run {} source".format(_class.name))
        _class.collect()
        if _class.urls:
            _class.save()

if __name__ == "__main__":
    main()
