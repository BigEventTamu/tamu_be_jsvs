# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0011_auto_20151208_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequeststub',
            name='email_address',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='jobrequeststub',
            name='full_name',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='jobrequeststub',
            name='phone_number',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
