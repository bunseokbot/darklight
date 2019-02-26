from elasticsearch_dsl import Document, Integer, Keyword, Text,\
                                Nested, Boolean, InnerDoc, Date


class Header(InnerDoc):
    name = Keyword()
    value = Keyword()


class Tree(InnerDoc):
    url = Keyword()
    status = Integer()
    content = Keyword()
    parent = Keyword()


class Webpage(Document):
    url = Keyword()
    domain = Keyword()
    title = Text()
    time = Date()
    screenshot = Keyword()
    source = Text()
    language = Keyword()
    headers = Nested(Header)
    tree = Nested(Tree)

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
