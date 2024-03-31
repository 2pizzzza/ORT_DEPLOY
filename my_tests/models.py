from django.db import models

from courses.models import Course
from users.models import User


class Test(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name="Описание")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses', verbose_name='Курс')
    next_test = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='previous_test', null=True, blank=True,
                                  verbose_name='следующий тест')

    class Meta:
        db_table = 'test'
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return f'Тест {self.title} по курсу {self.course.title}'


class TestUser(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='users', verbose_name='Тест')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests', verbose_name='Ученик')
    right_answers = models.PositiveIntegerField(verbose_name='Правильных ответов')

    class Meta:
        db_table = 'test_user'
        verbose_name = 'Пройденный тест'
        verbose_name_plural = 'Пройденные тесты'

    def __str__(self):
        return f'Тест {self.test.title} пройденный студентом {self.user.firstname} {self.user.lastname}'
