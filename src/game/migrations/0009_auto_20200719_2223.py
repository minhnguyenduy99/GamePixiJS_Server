# Generated by Django 3.0.8 on 2020-07-19 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20200719_2156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamestate',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='map',
            name='map_file',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='map',
            name='map_image',
            field=models.CharField(max_length=200),
        ),
    ]
