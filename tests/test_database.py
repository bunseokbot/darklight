from database.session import Session
from database.engine import Engine
from database.models import Domain

from utils.config.env import Env
from utils.config.ini import Ini


ini = Ini(Env.read('CONFIG_FILE'))


def test_create_engine():
    """
    Test for create a new engine
    :return:
    """
    assert Engine.create(ini=ini)


def test_database_session():
    """
    Test for connect database session
    :return:
    """
    engine = Engine.create(ini=ini)
    with Session(engine=engine) as session:
        assert session


def test_manage_model():
    """
    Test for create a new table at memory database
    :return:
    """
    engine = Engine.create(ini=ini)

    # add new data
    with Session(engine=engine) as session:
        session.add(Domain('test', 'https://formed_url.onion'))
        session.commit()

    with Session(engine=engine) as session:
        assert session.query(Domain).filter(Domain.uuid == 'test').count() == 1
        assert session.query(Domain).filter(Domain.uuid == 'is_not_exist').count() == 0
