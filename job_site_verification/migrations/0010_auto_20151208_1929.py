# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0009_auto_20151208_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequeststub',
            name='full_name',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
