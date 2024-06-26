from django.db import models

from my_tests import models as m
from main.settings import ANSWER_VIDEO_FOLDER, QUESTIONS_VIDEO_FOLDER



class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name='Вопрос')
    test = models.ForeignKey(m.Test, on_delete=models.CASCADE, related_name='questions', verbose_name='Тест')
    photo = models.ImageField(upload_to=QUESTIONS_VIDEO_FOLDER, verbose_name='Фото', null=True, blank=True)

    class Meta:
        db_table = 'questions'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'Вопрос {self.title}'


class Answer(models.Model):
    title = models.CharField(max_length=255, verbose_name='Ответ')
    correct = models.BooleanField(default=False, verbose_name='Правильный ответ')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    photo = models.ImageField(upload_to=ANSWER_VIDEO_FOLDER, verbose_name='Фото', null=True, blank=True)

    class Meta:
        db_table = 'answers'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        response = f'Ответ {self.title} на вопрос {self.question.title}'
        return f'Верный {response}' if self.correct else response
