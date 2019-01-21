from pipeline.elastic import Elastic
from pipeline.elastic.documents import Webpage, Service, Port

from utils.config.ini import Ini
from utils.config.env import Env


ini = Ini(Env.read('CONFIG_FILE'))


def test_start_connection():
    with Elastic(ini=ini) as conn:
        assert conn


def test_add_new_documents():
    with Elastic(ini=ini):
        webpage = Webpage(
            meta={'id': 1},
            url='https://www.test.onion',
            domain='www.test.onion',
            title='test title',
            screenshot='https://screenshot.link.dummy/test.jpg',
            language='ko',
        )
        webpage.source = """<html>
                <test>is it test?</test>
                </html>
                """
        webpage.save()

        assert Webpage.get(id=1)

        services = [
            Service(number=80, status=True),
            Service(number=443, status=False),
            Service(number=8080, status=False),
        ]

        Port(meta={'id': 1}, services=services).save()

        assert Port.get(id=1)

        # remove index after test
        Webpage._index.delete()
        Port._index.delete()
