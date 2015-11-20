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
            ],
        ),
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
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=20)),
                ('project_creation_date', models.DateTimeField(verbose_name=b'date published')),
                ('project_total_time', models.IntegerField(default=0)),
                ('project_yield', models.FloatField(default=0)),
                ('project_description', models.CharField(default=b'This is the description', max_length=600)),
                ('project_active_phase', models.CharField(default=b'', max_length=20)),
                ('project_active_iteration', models.CharField(default=b'', max_length=20)),
                ('project_status', models.CharField(default=b'PND', max_length=3, choices=[(b'ACT', b'Active'), (b'CLS', b'Closed'), (b'PND', b'Pending')])),
                ('creating_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phase', models.CharField(default=b'', max_length=20)),
                ('iteration', models.CharField(default=b'', max_length=20)),
                ('log_creation_date', models.DateTimeField(verbose_name=b'date published')),
                ('time_worked', models.DurationField()),
                ('work_type', models.CharField(default=b'DEV', max_length=3, choices=[(b'DEV', b'Development'), (b'DEF', b'Defect removal'), (b'MAN', b'Management')])),
                ('project', models.ForeignKey(to='ise_pdt.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
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
        migrations.AddField(
            model_name='defect',
            name='iteration_of_injection',
            field=models.ForeignKey(to='ise_pdt.Iteration'),
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
