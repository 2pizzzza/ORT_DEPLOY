from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

from . import validators as val


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields['role'] = 'Администратор'
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLES = (
        ('Учитель', 'Учитель'),
        ('Студент', 'Студент')
    )

    firstname = models.CharField(max_length=150, verbose_name='Имя')
    lastname = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, verbose_name='отчество')
    password = models.CharField(max_length=128, verbose_name='Пароль')
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, choices=ROLES, default=ROLES[1][1], null=True, verbose_name='Роль')

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.role} {self.firstname} {self.lastname}'

    def save(self, *args, **kwargs):
        if self.password and not str(self.password).startswith(('pbkdf2_sha256$', 'bcrypt')):
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Profile(models.Model):
    LANGUAGES = (
        ('Кыргызский', 'Кыргызский'),
        ('Русский', 'Русский'),
        ('Английский', 'Английский'),
    )

    SEX = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    language = models.CharField(max_length=50, choices=LANGUAGES, verbose_name='Язык')
    _class = models.CharField(max_length=4, validators=[val.validate_class], verbose_name='Класс')
    age = models.PositiveIntegerField(verbose_name="Возраст")
    sex = models.CharField(max_length=50, choices=SEX, verbose_name='Пол')
    phone = models.CharField(max_length=20, validators=[val.validate_phone], verbose_name='Номер телефона')
    school = models.CharField(max_length=100, verbose_name='Школа')
    university = models.CharField(max_length=100, verbose_name='Университет')
    specialization = models.CharField(max_length=100, verbose_name='Специальзация')

    class Meta:
        db_table = 'profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль студента {self.user.lastname} {self.user.firstname}'
