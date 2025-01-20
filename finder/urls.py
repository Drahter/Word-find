from django.urls import path
from django.views.decorators.cache import cache_page

from finder.apps import FinderConfig
from finder.views import (
    ArticleListView,
    ArticleCreateView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    IndexView, SearchView,
)

app_name = FinderConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('articles/', ArticleListView.as_view(),
         name='article_list'),
    path('articles/create/', ArticleCreateView.as_view(),
         name='article_create'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(),
         name='article_detail'),
    path('articles/<int:pk>/update/', ArticleUpdateView.as_view(),
         name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(),
         name='article_delete'),
    path('search/', SearchView.as_view(), name='search_request'),
]
