# Generated by Django 5.1.3 on 2024-11-23 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_favoritemovie_cart_alter_movie_actor'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='description_uz',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_name_ru',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_name_uz',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
