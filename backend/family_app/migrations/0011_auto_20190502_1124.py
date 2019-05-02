# Generated by Django 2.2 on 2019-05-02 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('family_app', '0010_auto_20190502_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marriage',
            name='_husband',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marriage_husband_set', related_query_name='marriages_husband', to='person_app.Person'),
        ),
        migrations.AlterField(
            model_name='marriage',
            name='_husbname',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marriage_husbname_set', related_query_name='marriages_husbname', to='core.SurName'),
        ),
        migrations.AlterField(
            model_name='marriage',
            name='_wife',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marriage_wife_set', related_query_name='marriages_wife', to='person_app.Person'),
        ),
        migrations.AlterField(
            model_name='marriage',
            name='_wifename',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marriage_wifename_set', related_query_name='marriages_wifename', to='core.SurName'),
        ),
    ]
