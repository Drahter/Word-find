from django.db import models
from django.contrib.postgres.fields import ArrayField

from finder.search import ArticleIndex


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

    def __str__(self):
        return f'Статья №{self.pk}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        article_doc = ArticleIndex(
            meta={'id': self.pk},
            rubrics=self.rubrics,
            text=self.text
        )
        article_doc.save()
        print('Document saved successfully')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['created_date']
