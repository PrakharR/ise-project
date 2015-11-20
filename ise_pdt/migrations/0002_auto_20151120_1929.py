# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ise_pdt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='project',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='defect',
            name='iteration_of_injection',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_active_iteration',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_active_phase',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_status',
        ),
        migrations.RemoveField(
            model_name='timelog',
            name='iteration',
        ),
        migrations.RemoveField(
            model_name='timelog',
            name='phase',
        ),
        migrations.AlterField(
            model_name='project',
            name='project_description',
            field=models.CharField(max_length=600),
        ),
        migrations.DeleteModel(
            name='Assignment',
        ),
        migrations.DeleteModel(
            name='Defect',
        ),
    ]
