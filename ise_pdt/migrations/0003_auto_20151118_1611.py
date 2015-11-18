# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ise_pdt', '0002_project_user_in_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iteration_name', models.CharField(max_length=20)),
                ('iteration_start_date', models.DateTimeField(verbose_name=b'date published')),
                ('iteration_status', models.CharField(max_length=3, choices=[(b'ACT', b'Active'), (b'CLS', b'Closed'), (b'PND', b'Pending')])),
                ('iteration_estimate_SLOC', models.IntegerField(default=0)),
                ('iteration_SLOC', models.IntegerField(default=0)),
                ('iteration_estimate_effort', models.FloatField()),
                ('iteration_effort', models.FloatField()),
                ('iteration_defect_injected', models.IntegerField(default=0)),
                ('iteration_defect_removed', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phase_name', models.CharField(max_length=4, choices=[(b'INCP', b'Inception'), (b'ELAB', b'Elaboration'), (b'CONS', b'Sonstruction'), (b'TRAN', b'Transition')])),
                ('phase_start_date', models.DateTimeField(verbose_name=b'date published')),
                ('phase_status', models.CharField(max_length=3, choices=[(b'ACT', b'Active'), (b'CLS', b'Closed'), (b'PND', b'Pending')])),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='user_in_project',
        ),
        migrations.AddField(
            model_name='project',
            name='project_yield',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='timelog',
            name='work_type',
            field=models.CharField(default=b'DEV', max_length=3, choices=[(b'DEV', b'Development'), (b'DEF', b'Defect removal'), (b'MAN', b'Management')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='creating_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='timelog',
            name='time_worked',
            field=models.DurationField(),
        ),
        migrations.AlterField(
            model_name='timelog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='phase',
            name='project',
            field=models.ForeignKey(to='ise_pdt.Project'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='phase',
            field=models.ForeignKey(to='ise_pdt.Phase'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='project',
            field=models.ForeignKey(to='ise_pdt.Project'),
        ),
    ]
