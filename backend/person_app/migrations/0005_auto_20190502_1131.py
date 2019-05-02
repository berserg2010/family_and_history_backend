# Generated by Django 2.2 on 2019-05-02 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person_app', '0004_auto_20190502_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birth',
            name='changer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_app_birth_changer_set', related_query_name='person_app_births_changer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='birth',
            name='submitter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_app_birth_submitter_set', related_query_name='person_app_births_submitter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='changer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_app_person_changer_set', related_query_name='person_app_persons_changer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='submitter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person_app_person_submitter_set', related_query_name='person_app_persons_submitter', to=settings.AUTH_USER_MODEL),
        ),
    ]
