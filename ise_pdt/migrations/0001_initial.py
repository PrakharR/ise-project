# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=20)),
                ('project_creation_date', models.DateTimeField(verbose_name=b'date published')),
                ('project_total_time', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_creation_date', models.DateTimeField(verbose_name=b'date published')),
                ('time_worked', models.IntegerField(default=0)),
                ('project', models.ForeignKey(to='ise_pdt.Project')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=20)),
                ('user_email', models.CharField(max_length=100)),
                ('user_password', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='timelog',
            name='user',
            field=models.ForeignKey(to='ise_pdt.User'),
        ),
        migrations.AddField(
            model_name='project',
            name='creating_user',
            field=models.ForeignKey(to='ise_pdt.User'),
        ),
    ]
