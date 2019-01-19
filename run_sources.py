"""
Run all sources to collect domain from registered sources.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""
from utils.logging.log import Log

import source as sources


def main():
    """Main method for running all sources."""
    Log.i("{} source(s) detected!".format(len(sources.__all__)))

    for source in sources.__all__:
        _class = source()
        if _class.active:
            Log.i("Trying to run {} source".format(_class.name))
            try:
                _class.collect()
            except:
                Log.e("Failed to collect data from {} source".format(_class.name))
            if _class.urls:
                _class.save()
        else:
            Log.i("{} source is now disabled".format(_class.name))

        del _class

if __name__ == "__main__":
    main()
