from utils.logging.log import Log


def test_write_debug():
    Log.d("Test Debugging Message")


def test_write_info():
    Log.i("Test Info Message")


def test_write_warning():
    Log.w("Test Warning Message")


def test_write_error():
    Log.e("Test Error Message")


def test_write_critical():
    Log.c("Test Critical Message")
