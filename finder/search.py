from elasticsearch_dsl import Document, Text


class DocumentIndex(Document):
    rubrics = Text(analyzer='russian')
    text = Text(analyzer='russian')

    class Index:
        name = 'documents'
