# Generated by Django 2.2 on 2019-05-02 08:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person_app', '0003_auto_20190428_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birth',
            name='_likes',
            field=models.ManyToManyField(blank=True, related_name='person_app_birth_likes_set', related_query_name='person_app_births_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
