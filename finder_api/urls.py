from django.urls import path
from finder_api.apps import FinderApiConfig
from finder_api.views import LessonRetrieveAPIView

app_name = FinderApiConfig.name

urlpatterns = [
    path('articles/<int:pk>/', LessonRetrieveAPIView.as_view(), name='api_article_detail'),
]