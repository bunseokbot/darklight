from sqlalchemy.orm import sessionmaker


class Session():
    """
    Connect database engine and manage session
    """
    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.dbsession = sessionmaker(bind=self.engine)()
        return self.dbsession

    def __exit__(self, *args):
        self.dbsession.close()
