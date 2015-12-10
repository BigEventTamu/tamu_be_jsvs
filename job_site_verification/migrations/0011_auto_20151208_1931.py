# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_site_verification', '0010_auto_20151208_1929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobrequeststub',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='jobrequeststub',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='jobrequeststub',
            name='phone_number',
        ),
    ]
