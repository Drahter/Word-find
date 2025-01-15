from elasticsearch import NotFoundError
from elasticsearch_dsl import Search

from finder.models import Article
from finder.search import ArticleIndex


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
    article_doc = ArticleIndex(
        meta={'id': article.id},
        rubrics=article.rubrics,
        text=article.text
    )
    article_doc.save()
    print('Document saved successfully')


def delete_article_doc(doc_id):
    try:
        article = Article.objects.get(id=doc_id)
        doc = Search(index='articles').query('match', id=doc_id)
        doc.delete()
        print("Document deleted")
    except NotFoundError:
        print("Document not found in Elasticsearch")
