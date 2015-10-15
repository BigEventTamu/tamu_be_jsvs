# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of Service', max_length=100)),
                ('description', models.TextField(help_text=b'Description of Service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('is_current', models.BooleanField(default=True, help_text=b'Is available for customer to complete')),
                ('service', models.ForeignKey(help_text=b'Which service is this form for?', to='job_site_verification.Service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceFormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_label', models.CharField(help_text=b'Ex: How many accounts?', max_length=150, verbose_name=b'Prompt')),
                ('field_type', models.CharField(max_length=32, choices=[(b'CharField', b'Character Field'), (b'TextField', b'Open Ended Text Field'), (b'BooleanField', b'Boolean Field'), (b'ChoiceField', b'Choice Field'), (b'ChoiceCharField', b'Choice Field with "Other" prompt'), (b'EmailField', b'Email Address Field')])),
                ('help_text', models.CharField(help_text=b'Help text looks like this. May leave blank', max_length=150, null=True, blank=True)),
                ('position', models.IntegerField(default=1000, blank=True)),
                ('required', models.BooleanField(default=True, help_text=b'Can user leave this field blank?')),
                ('form', models.ForeignKey(to='job_site_verification.ServiceForm')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceFormFieldChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=128)),
                ('field', models.ForeignKey(to='job_site_verification.ServiceFormField')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRequestForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.DateTimeField(auto_now=True)),
                ('form', models.ForeignKey(to='job_site_verification.ServiceForm')),
                ('requested_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(to='job_site_verification.Service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRequestFormFieldAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
                ('field', models.ForeignKey(to='job_site_verification.ServiceFormField')),
                ('form', models.ForeignKey(to='job_site_verification.ServiceRequestForm')),
            ],
        ),
    ]
