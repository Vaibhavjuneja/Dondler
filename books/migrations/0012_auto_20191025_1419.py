# Generated by Django 2.2.6 on 2019-10-25 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_auto_20191025_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicresources',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
