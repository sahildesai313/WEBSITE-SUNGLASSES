# Generated by Django 5.0.1 on 2024-03-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glasses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
