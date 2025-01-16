from django.apps import AppConfig
from elasticsearch_dsl import connections

from config.settings import ELASTICSEARCH_HOSTS
from finder.documents import ArticleDocument


class FinderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finder'

    def ready(self):
        """
        Функция создает соединение с базой ElasticSeach и инициализирует индекс для работы со статьями.
        """
        connections.create_connection(hosts=ELASTICSEARCH_HOSTS)

        if not ArticleDocument._index.exists():
            ArticleDocument.init()  # Инициализация индекса в Elasticsearch
            print("Index created")
