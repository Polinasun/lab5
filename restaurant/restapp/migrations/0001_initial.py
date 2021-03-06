# Generated by Django 2.2.7 on 2019-11-18 14:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('menu_category', models.CharField(choices=[('0', 'breakfast'), ('1', 'lunch'), ('2', 'dinner')], max_length=1)),
                ('number_room', models.IntegerField()),
                ('room_id', models.UUIDField(default=uuid.uuid4)),
                ('guest', models.UUIDField(default=uuid.uuid4)),
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
    ]
