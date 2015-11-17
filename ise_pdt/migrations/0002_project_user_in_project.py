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
            name='user_in_project',
            field=models.CharField(default='PrakharRathi', max_length=20),
            preserve_default=False,
        ),
    ]
