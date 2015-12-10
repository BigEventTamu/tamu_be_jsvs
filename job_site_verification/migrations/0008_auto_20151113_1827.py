# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0007_auto_20151022_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequeststub',
            name='job_zone',
            field=models.CharField(default=1, max_length=4, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobrequeststub',
            name='job_zone_team',
            field=models.CharField(default='1a', max_length=4, db_index=True),
            preserve_default=False,
        ),
    ]
