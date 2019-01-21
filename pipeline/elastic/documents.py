from elasticsearch_dsl import Document, Integer, Keyword, Text,\
                                Nested, Boolean, InnerDoc, Index


class Webpage(Document):
    url = Keyword()
    domain = Keyword()
    title = Text()
    screenshot = Keyword()
    source = Text()
    language = Keyword()

    class Index:
        name = 'webpage'
        settings = {
            'number_of_shards': 2,
        }


class Service(InnerDoc):
    number = Integer()
    status = Boolean()


class Port(Document):
    services = Nested(Service)

    class Index:
        name = 'port'
        settings = {
            'number_of_shards': 2,
        }
