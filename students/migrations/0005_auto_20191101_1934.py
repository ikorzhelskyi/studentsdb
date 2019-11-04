# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_monthjournal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
        migrations.AlterModelOptions(
            name='monthjournal',
            options={'verbose_name': 'Monthly Journal', 'verbose_name_plural': 'Monthly Journals'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Student', verbose_name='Leader'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='notes',
            field=models.TextField(verbose_name='Extra Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='date',
            field=models.DateField(verbose_name='Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='student',
            field=models.ForeignKey(unique_for_month=b'date', verbose_name='Student', to='students.Student'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Birthday'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='First Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='Last Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(default=b'', max_length=256, verbose_name='Middle Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(verbose_name='Extra Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Group', to='students.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.CharField(max_length=256, verbose_name='Ticket'),
            preserve_default=True,
        ),
    ]
