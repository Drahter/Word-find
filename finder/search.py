from elasticsearch_dsl import Document, Text, Keyword


class DocumentIndex(Document):
    rubrics = Keyword()
    text = Text()

    class Index:
        name = 'documents'
