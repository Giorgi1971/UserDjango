# Generated by Django 4.0.3 on 2022-03-29 09:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_comment_alter_post_created_delete_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='mes_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 13, 57, 34, 634401)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 29, 13, 57, 34, 632401)),
        ),
    ]
