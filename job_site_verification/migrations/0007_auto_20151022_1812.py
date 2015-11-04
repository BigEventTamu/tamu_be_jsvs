# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_site_verification', '0006_auto_20151021_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequeststub',
            name='reserved_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='jobrequeststub',
            name='job_request_id',
            field=models.CharField(max_length=16, db_index=True),
        ),
    ]
