# Generated by Django 2.2 on 2019-04-11 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_app', '0006_auto_20190411_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='child',
            field=models.ManyToManyField(through='family_app.Child', to='person_app.Birth'),
        ),
    ]