# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vmaig_system', '0002_auto_20160410_1420'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-create_time'], 'verbose_name': '\u6d88\u606f', 'verbose_name_plural': '\u6d88\u606f'},
        ),
    ]
