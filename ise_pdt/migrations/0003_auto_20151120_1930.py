# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ise_pdt', '0002_auto_20151120_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignment_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('defect_type', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('iteration_of_injection', models.ForeignKey(to='ise_pdt.Iteration')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='project_active_iteration',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='project',
            name='project_active_phase',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='project',
            name='project_status',
            field=models.CharField(default=b'PND', max_length=3, choices=[(b'ACT', b'Active'), (b'CLS', b'Closed'), (b'PND', b'Pending')]),
        ),
        migrations.AddField(
            model_name='timelog',
            name='iteration',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AddField(
            model_name='timelog',
            name='phase',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_description',
            field=models.CharField(default=b'This is the description', max_length=600),
        ),
        migrations.AddField(
            model_name='assignment',
            name='project',
            field=models.ForeignKey(to='ise_pdt.Project'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
