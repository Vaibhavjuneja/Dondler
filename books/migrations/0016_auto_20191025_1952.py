# Generated by Django 2.2.6 on 2019-10-25 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_topicuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicuser',
            name='count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
