from elasticsearch_dsl import Document, Text, Date, Keyword
from .models import Article


class ArticleDocument(Document):
    rubrics = Keyword(multi=True)
    text = Text()
    created_date = Date()
    owner = Keyword()

    class Index:
        name = 'articles'  # Name of the Elasticsearch index

    @classmethod
    def get_document(cls, article):
        return cls(
            meta={'id': article.pk},
            rubrics=article.rubrics,
            text=article.text,
            created_date=article.created_date,
            owner=article.owner.pk if article.owner else None
        )
