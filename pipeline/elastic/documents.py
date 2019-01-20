from elasticsearch_dsl import Document, Integer, Keyword, Text, Nested, Boolean


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


class Port(Document):
    services = Nested(
        include_in_parent=True,
        properties={
            'number': Integer(),
            'status': Boolean()
        }
    )

    class Index:
        name = 'port'
        settings = {
            'number_of_shards': 2,
        }
