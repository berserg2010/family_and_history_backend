from django.contrib.auth import get_user_model
from django.db import models


class ObjectField(models.Model):
    note = models.TextField(
        blank=True,
        null=True,
        default='',
    )
    submitted = models.DateTimeField(
        auto_now_add=True,
    )
    submitter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='%(app_label)s_%(class)s_submitter_set',
        related_query_name='%(app_label)s_%(class)ss_submitter',

    )
    changed = models.DateTimeField(
        auto_now=True,
    )
    changer = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='%(app_label)s_%(class)s_changer_set',
        related_query_name='%(app_label)s_%(class)ss_changer',
    )

    class Meta:
        abstract = True
