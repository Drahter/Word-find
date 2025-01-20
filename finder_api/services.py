from finder.documents import ArticleDocument


def api_get_results(query):
    """
    Функция для запросов к Elasticsearch.

    Args:
        query: string
    Returns:
        list of dicts
        список словарей с содержимым статей, подходящих
        по параметрам поиска.
    """
    search = ArticleDocument.search().query("multi_match", query=query, fields=['rubrics', 'text'])
    search = search[:20]
    response = search.execute()

    results = [
        {
            'id': hit.meta.id,
            'rubrics': hit.rubrics,
            'text': hit.text
        }
        for hit in response
    ]
    return results
