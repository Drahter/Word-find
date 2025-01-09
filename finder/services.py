from elasticsearch_dsl import Search


def get_results(request):
    # Создаем объект поиска
    search = Search(index='documents')

    # Добавляем сложные условия поиска
    search = search.query('multi_match', query=request, fields=['rubrics', 'text'])

    response = search.execute()

    return response
