from django.db import models

from main.settings import NEWS_IMAGE_FOLDER


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    image = models.ImageField(upload_to=NEWS_IMAGE_FOLDER, verbose_name='Фото')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'Новость {self.title}'
