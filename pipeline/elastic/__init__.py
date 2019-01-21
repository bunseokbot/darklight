from elasticsearch_dsl.connections import connections

from .documents import Webpage, Port


class Elastic:
    """
    Create new elasticsearch connection.
    """
    def __init__(self, ini):
        self.ini = ini

    def __enter__(self):
        connection = connections.create_connection(
            hosts=['{}:{}'.format(
                self.ini.read('ELASTICSEARCH', 'HOST'),
                self.ini.read('ELASTICSEARCH', 'PORT')
            )]
        )

        # create when index not exist
        if not Webpage._index.exists():
            Webpage._index.create()

        if not Port._index.exists():
            Port._index.create()

        return connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
