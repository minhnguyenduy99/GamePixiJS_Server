# Generated by Django 3.0.8 on 2020-07-19 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20200719_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='created_by',
            field=models.IntegerField(),
        ),
    ]
