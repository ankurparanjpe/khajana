# Generated by Django 3.0.5 on 2020-06-15 18:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200616_0000'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='weather',
            new_name='City',
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 15, 18, 39, 5, 573492, tzinfo=utc)),
        ),
    ]