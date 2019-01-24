"""
Run all sources to collect domain from registered sources.

Developed by Namjun Kim (bunseokbot@gmail.com)
"""
from apscheduler.schedulers.background import BackgroundScheduler

from utils.logging.log import Log

import source as sources

import time


def run(source):
    _class = source()
    status = _class.active

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

    return status


def main():
    """Main method for running all sources."""
    scheduler = BackgroundScheduler()
    scheduler.start()

    Log.i("{} source(s) detected!".format(len(sources.__all__)))

    job_id = 1

    for source in sources.__all__:
        status = run(source)  # initial run source.

        if status:
            # register a scheduler for running periodically. (only for active source)
            scheduler.add_job(run, "interval",
                              minutes=source().cycle, id=str(job_id),
                              args=(source, ))
            Log.i("Successfully add a new job")

            job_id += 1

    while True:
        time.sleep(60)  # sleep 1 mintue for running scheduler normally.

    scheduler.shutdown()

if __name__ == "__main__":
    main()
