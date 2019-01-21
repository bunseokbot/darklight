from elasticsearch_dsl.connections import connections


class Elastic:
    """
    Create new elasticsearch connection.
    """
    def __init__(self, ini):
        self.ini = ini

    def __enter__(self):
        return connections.create_connection(
            hosts=['{}:{}'.format(
                self.ini.read('ELASTICSEARCH', 'HOST'),
                self.ini.read('ELASTICSEARCH', 'PORT')
            )]
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
