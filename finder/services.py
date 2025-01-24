from elasticsearch import NotFoundError
from elasticsearch_dsl import Search

from finder.documents import ArticleDocument
from finder.models import Article

"""Функции для взаимодействия с ElasticSearch"""


def get_search_results(query):
    """
    Выполняет запрос к базе данных ES и обрабатывает ответ

    Args:
        query: string
    Returns:
        list: список объектов Article

    Выдача ограничена двадцатью последними внесенными статьями

    """
    # Создаем объект поиска
    search = Search(index='articles')

    # Задаем условия поиска, передавая параметр query
    search = search.query(
        'multi_match',
        query=query,
        fields=['rubrics', 'text']
    )

    response = search.execute()
    results = []
    for hit in response:
        results.append(Article.objects.get(id=hit.meta.id))
    sorted(results, key=lambda x: x.created_date)
    results = results[-20:]

    return results



def save_article_doc(article):
    """
    Создает документ в ES из объекта Article

    Args:
        article: объект модели Article

    Returns:
        None
    """
    article_doc = ArticleDocument(
        meta={'id': article.id},
        rubrics=', '.join(article.rubrics),
        text=article.text,
        owner=article.owner.pk,
        created_date=article.created_date
    )
    article_doc.save()
    print('Document saved successfully')


def delete_article_doc(doc_id):
    """
    Удаляет документ из ES по его id

    Args:
        doc_id: id документа

    Returns:
        None
    """
    try:
        article_document = ArticleDocument.get(id=doc_id)
        article_document.delete()
        print("Document deleted")
    except NotFoundError:
        print("Document not found in Elasticsearch")
