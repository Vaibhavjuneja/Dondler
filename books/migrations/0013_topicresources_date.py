# Generated by Django 2.2.6 on 2019-10-25 16:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_auto_20191025_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicresources',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
