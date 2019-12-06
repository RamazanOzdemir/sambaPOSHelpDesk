# Generated by Django 2.2.7 on 2019-12-05 12:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0005_auto_20191205_1458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='messageblock',
            name='uid',
            field=models.CharField(default=uuid.UUID('28e9823c-24be-4ab6-8bc4-e6a4e20f2c3e'), max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='uid',
            field=models.CharField(default=uuid.UUID('874aaefe-4236-4abf-a4b1-21331d471c6c'), max_length=50),
        ),
    ]
