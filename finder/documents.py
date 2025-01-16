from elasticsearch_dsl import Document, Text, Date, Keyword


class ArticleDocument(Document):
    """
    Описание индекса статей для Elasticearch

    Поля:
    rubrics - список ключевых слов статьи
    text - текст статьи
    created_date - дата создания статьи
    owner - идентификатор автора статьи
    """
    rubrics = Text()
    text = Text()
    created_date = Date()
    owner = Keyword()

    class Index:
        """Имя индекса в ElasticSearch"""
        name = 'articles'

    @classmethod
    def get_document(cls, article):
        """Создание документа из модели Article"""
        return cls(
            meta={'id': article.pk},
            rubrics=article.rubrics,
            text=article.text,
            created_date=article.created_date,
            owner=article.owner.pk if article.owner else None
        )
