from elasticsearch_dsl import Document, Text


class ArticleIndex(Document):
    rubrics = Text(analyzer='russian')
    text = Text(analyzer='russian')

    class Index:
        name = 'articles'
