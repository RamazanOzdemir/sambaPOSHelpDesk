# Generated by Django 2.2.7 on 2019-12-05 10:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageblock',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tag', to='mails.Tag'),
        ),
        migrations.AlterField(
            model_name='messageblock',
            name='uid',
            field=models.CharField(default=uuid.UUID('ed2f3add-2791-414a-8a65-3fa605ffac4c'), max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='uid',
            field=models.CharField(default=uuid.UUID('8038b9a1-a1dd-4076-95e7-658971fea3a7'), max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='wait_to_reply',
            field=models.ManyToManyField(blank=True, related_name='incomingemails', to='mails.MessageBlock'),
        ),
    ]