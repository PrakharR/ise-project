# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ise_pdt', '0005_auto_20151118_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelog',
            name='time_worked',
            field=models.IntegerField(default=0),
        ),
    ]
