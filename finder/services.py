from elasticsearch import NotFoundError
from elasticsearch_dsl import Search

from finder.documents import ArticleDocument
from finder.models import Article


def get_results(request):
    # Создаем объект поиска
    search = Search(index='articles')

    # Добавляем сложные условия поиска
    search = search.query('multi_match', query=request, fields=['rubrics', 'text'])

    response = search.execute()
    results = []
    for hit in response:
        results.append(Article.objects.get(id=hit.meta.id))
    results = results[-20:][::-1]

    return results


def save_article_doc(article):
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
    try:
        article_document = ArticleDocument.get(id=doc_id)
        article_document.delete()
        print("Document deleted")
    except NotFoundError:
        print("Document not found in Elasticsearch")
