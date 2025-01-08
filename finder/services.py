from elasticsearch_dsl import Search


def get_results(request):
    # Создаем объект поиска
    search = Search(index='documents')

    # Добавляем сложные условия поиска
    search = search.query(
        {"match": {"content": request}},  # Должен содержать "example"
    )

    response = search.execute()

    # Обработка результатов
    for hit in response:
        print(f'Title: {hit.title}, Tags: {hit.tags}, Content: {hit.content}')

    return response
