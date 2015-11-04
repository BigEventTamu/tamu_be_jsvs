# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0003_auto_20151021_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequeststub',
            name='lat',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AddField(
            model_name='jobrequeststub',
            name='lon',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True),
        ),
    ]
