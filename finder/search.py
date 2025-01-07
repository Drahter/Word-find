from elasticsearch_dsl import Document, Text, Keyword, connections

# Создаем соединение с Elasticsearch
connections.create_connection(hosts=['http://elasticsearch:9200'])


class DocumentIndex(Document):
    rubrics = Keyword()
    text = Text()

    class Index:
        name = 'documents'


DocumentIndex.init()
print("Index created")

if __name__ == '__main__':
    if not DocumentIndex._index.exists():
        DocumentIndex.init()  # Инициализация индекса в Elasticsearch
        print("Index created")
