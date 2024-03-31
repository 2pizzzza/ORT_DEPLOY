from django.core.validators import FileExtensionValidator
from django.db import models

from courses.models import Course
from main.settings import TEST_VIDEO_FOLDER
from my_tests.models import Test
from users.models import User


class Video(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    video = models.FileField(upload_to=TEST_VIDEO_FOLDER, validators=[FileExtensionValidator(allowed_extensions=['mp4'])], verbose_name="Видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    user_watched = models.ManyToManyField(User, related_name='watched_videos', blank=True, verbose_name="Просмотревшие")
    test = models.OneToOneField(Test, on_delete=models.CASCADE, related_name='video', blank=True, null=True, verbose_name="Тест к видео")

    class Meta:
        db_table = 'video'
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'

    def __str__(self):
        return f'Видео {self.title} по курсу {self.course.title}'
