# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ise_pdt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_description',
            field=models.CharField(default='This is the project description', max_length=200),
            preserve_default=False,
        ),
    ]
