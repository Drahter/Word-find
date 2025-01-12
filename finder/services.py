from elasticsearch_dsl import Search

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
