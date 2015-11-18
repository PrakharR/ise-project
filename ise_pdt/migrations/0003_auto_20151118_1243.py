# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ise_pdt', '0002_project_user_in_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_creation_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='timelog',
            name='log_creation_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
