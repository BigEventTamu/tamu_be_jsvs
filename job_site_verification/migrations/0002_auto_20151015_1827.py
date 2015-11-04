# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceformfield',
            name='field_type',
            field=models.CharField(max_length=32, choices=[(b'CharField', b'Character Field'), (b'TextField', b'Open Ended Text Field'), (b'BooleanField', b'Boolean Field'), (b'ChoiceField', b'Choice Field'), (b'ChoiceCharField', b'Choice Field with "Other" prompt'), (b'EmailField', b'Email Address Field'), (b'IntegerField', b'Integer Field')]),
        ),
        migrations.AlterField(
            model_name='servicerequestform',
            name='requested_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
