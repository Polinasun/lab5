# Generated by Django 2.2.7 on 2019-12-05 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guestapp', '0002_auto_20191205_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guests',
            name='room_id',
            field=models.UUIDField(default=None),
        ),
    ]