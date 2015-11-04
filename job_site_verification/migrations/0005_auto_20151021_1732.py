# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0004_auto_20151021_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequeststub',
            name='job_state',
            field=models.CharField(default=b'needs_survey', max_length=32, db_index=True, choices=[(b'needs_survey', b'Needs Survey'), (b'survey_completed', b'Survey Completed')]),
        ),
    ]
