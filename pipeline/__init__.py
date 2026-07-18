class Pipeline:
    """Custom pipeline base class for adding custom pipeline."""
    active = True  # Pipeline active status

    def __init__(self, domain, data, ini):
        self.data = data  # DynamicObject type
        self.ini = ini
        self.domain = domain

    def handle(self):
        """Custom pipeline handler."""
        pass

    def __del__(self):
        del self
