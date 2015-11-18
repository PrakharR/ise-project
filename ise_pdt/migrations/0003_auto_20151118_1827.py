# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ise_pdt', '0002_project_project_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_description',
            field=models.CharField(max_length=600),
        ),
    ]
