# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0002_auto_20151015_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobRequestStub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_request_id', models.IntegerField()),
                ('job_description', models.TextField(max_length=2048)),
                ('job_state', models.CharField(default=b'needs_survey', max_length=32, choices=[(b'needs_survey', b'Needs Survey'), (b'survey_completed', b'Survey Completed')])),
                ('address_1', models.CharField(max_length=b'128', null=True, blank=True)),
                ('address_2', models.CharField(max_length=b'128', null=True, blank=True)),
                ('zip_code', models.CharField(max_length=b'16', null=True, blank=True)),
                ('city', models.CharField(max_length=b'128', null=True, blank=True)),
                ('state', models.CharField(max_length=b'16', null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='servicerequestform',
            name='job_stub',
            field=models.ForeignKey(blank=True, to='job_site_verification.JobRequestStub', null=True),
        ),
    ]
