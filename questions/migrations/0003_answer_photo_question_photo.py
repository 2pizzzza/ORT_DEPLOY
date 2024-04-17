# Generated by Django 5.0.2 on 2024-04-11 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_alter_answer_correct_alter_answer_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='tests/answer', verbose_name='Фото'),
        ),
        migrations.AddField(
            model_name='question',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='tests/images', verbose_name='Фото'),
        ),
    ]
