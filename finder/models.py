from django.db import models
from django.contrib.postgres.fields import ArrayField


class Document(models.Model):
    rubrics = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True,
        verbose_name='Рубрики документа'
    )

    text = models.TextField(verbose_name='Текст документа')

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления документа'
    )

    def __str__(self):
        return f'Документ №{self.pk}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-created_date']
