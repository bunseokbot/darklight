from sqlalchemy import create_engine

from utils.logging.log import Log

from .models import Base


class Engine:

    @classmethod
    def create(cls, ini):
        Log.d("Creating database engine...")
        engine = create_engine(ini.read('DATABASE', 'URL'),
            echo=True if ini.read('DATABASE', 'DEBUG') is 'true' else False)
        Base.metadata.create_all(bind=engine)
        return engine
