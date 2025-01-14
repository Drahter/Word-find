from django.db import models
from django.contrib.postgres.fields import ArrayField

from finder.search import ArticleIndex
from config.settings import AUTH_USER_MODEL


class Article(models.Model):
    rubrics = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True,
        verbose_name='Рубрики статьи'
    )

    text = models.TextField(verbose_name='Текст статьи')

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления статьи'
    )

    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name='автор статьи',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'Статья №{self.pk}'


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['created_date']
