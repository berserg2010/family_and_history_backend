# Generated by Django 2.2 on 2019-05-02 08:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_app', '0011_auto_20190502_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marriage',
            name='_likes',
            field=models.ManyToManyField(blank=True, related_name='family_app_marriage_likes_set', related_query_name='family_app_marriages_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]