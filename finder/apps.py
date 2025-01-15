from django.apps import AppConfig
from elasticsearch_dsl import connections

from finder.documents import ArticleDocument


class FinderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finder'

    def ready(self):
        # Создаем соединение с Elasticsearch
        connections.create_connection(hosts=['http://elasticsearch:9200'])

        if not ArticleDocument._index.exists():
            ArticleDocument.init()  # Инициализация индекса в Elasticsearch
            print("Index created")
