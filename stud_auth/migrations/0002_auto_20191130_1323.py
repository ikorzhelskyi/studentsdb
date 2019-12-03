# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stud_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stprofile',
            options={'verbose_name': '\u041f\u0440\u043e\u0444\u0456\u043b\u044c \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430'},
        ),
        migrations.AlterField(
            model_name='stprofile',
            name='mobile_phone',
            field=models.CharField(default=b'', max_length=12, verbose_name='\u041c\u043e\u0431\u0456\u043b\u044c\u043d\u0438\u0439 \u0442\u0435\u043b\u0435\u0444\u043e\u043d', blank=True),
            preserve_default=True,
        ),
    ]
