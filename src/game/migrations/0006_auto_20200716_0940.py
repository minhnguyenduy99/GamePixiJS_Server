# Generated by Django 3.0.8 on 2020-07-16 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_map_map_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='map_file',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='map',
            name='map_image',
            field=models.URLField(),
        ),
    ]
