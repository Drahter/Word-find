from elasticsearch_dsl import Search

from finder.models import Document


def get_results(request):
    # Создаем объект поиска
    search = Search(index='documents')

    # Добавляем сложные условия поиска
    search = search.query('multi_match', query=request, fields=['rubrics', 'text'])

    response = search.execute()
    results = []
    for hit in response:
        results.append(Document.objects.get(id=hit.meta.id))

    return results
