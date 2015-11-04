# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0005_auto_20151021_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrequeststub',
            name='job_request_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='jobrequeststub',
            name='job_state',
            field=models.CharField(default=b'needs_survey', max_length=32, db_index=True, choices=[(b'survey_canceled', b'Survey Canceled'), (b'needs_survey', b'Needs Survey'), (b'survey_completed', b'Survey Completed')]),
        ),
    ]
