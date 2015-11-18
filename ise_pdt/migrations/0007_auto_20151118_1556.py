# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ise_pdt', '0006_auto_20151118_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelog',
            name='time_worked',
            field=models.DurationField(),
        ),
    ]
