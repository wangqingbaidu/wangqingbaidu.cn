# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u6807\u9898')),
                ('url', models.CharField(max_length=200, null=True, verbose_name='\u8fde\u63a5', blank=True)),
                ('type', models.CharField(max_length=20, null=True, verbose_name='\u7c7b\u578b', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u53cb\u60c5\u94fe\u63a5',
                'verbose_name_plural': '\u53cb\u60c5\u94fe\u63a5',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u6807\u9898')),
                ('text', models.TextField(verbose_name='\u5185\u5bb9')),
                ('url', models.CharField(max_length=200, null=True, verbose_name='\u8fde\u63a5', blank=True)),
                ('type', models.CharField(max_length=20, null=True, verbose_name='\u7c7b\u578b', blank=True)),
                ('is_read', models.IntegerField(default=0, verbose_name='\u662f\u5426\u8bfb\u8fc7', choices=[(0, '\u672a\u8bfb'), (1, '\u5df2\u8bfb')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('from_user', models.ForeignKey(related_name='from_user_notification_set', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u53d1\u9001\u8005')),
                ('to_user', models.ForeignKey(related_name='to_user_notification_set', verbose_name='\u63a5\u6536\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u6d88\u606f',
                'verbose_name_plural': '\u6d88\u606f',
            },
        ),
    ]
