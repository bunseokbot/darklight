from utils.logging.log import Log


class Pipeline:
    """Pipeline class for adding additional data from original source."""

    def __init__(self, obj):
        self.object = obj

    def execute(self):
        """
        Execute pipeline and save it.
        :return:
        """
        pass

    def __del__(self):
        del self
