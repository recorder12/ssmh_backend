# Generated by Django 2.2 on 2022-05-15 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles_api', '0002_auto_20220515_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilefeeditem',
            name='popularityName',
        ),
        migrations.RemoveField(
            model_name='profilefeeditem',
            name='popularityValue',
        ),
        migrations.RemoveField(
            model_name='profilefeeditem',
            name='sourceOrder',
        ),
    ]
