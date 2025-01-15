from finder.documents import ArticleDocument


def api_get_results(query):
    search = ArticleDocument.search().query("multi_match", query=query, fields=['rubrics', 'text'])
    search = search[:20]
    response = search.execute()

    results = [
        {
            'id': hit.meta.id,
            'rubrics': ', '.join(hit.rubrics),
            'text': hit.text
        }
        for hit in response
    ]
    return results
