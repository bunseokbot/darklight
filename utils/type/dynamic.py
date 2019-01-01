class DynamicObject:
    """Dynamic object type for handling dict as python object."""
    def __init__(self, data={}):
        self.__dict__ = data

    def pop(self, key):
        return self.__dict__.pop(key)

    def is_empty(self):
        # check if data is empty
        return self.__dict__ == {}
