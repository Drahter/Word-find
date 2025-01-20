from django.urls import path
from drf_yasg import openapi

from finder_api.apps import FinderApiConfig
from finder_api.views import LessonRetrieveAPIView, APISearchView

api_info = openapi.Info(
    title="Finder API",
    default_version='v1',
    description="API for finding words in articles"
)

app_name = FinderApiConfig.name

urlpatterns = [
    path('articles/<int:pk>/', LessonRetrieveAPIView.as_view(), name='api_article_detail'),
    path('search/', APISearchView.as_view(), name='api_search'),
]
