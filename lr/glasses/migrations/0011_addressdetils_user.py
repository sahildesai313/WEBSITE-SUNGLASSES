# Generated by Django 5.0 on 2024-02-28 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glasses', '0010_alter_addressdetils_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressdetils',
            name='user',
            field=models.CharField(default='', max_length=10),
        ),
    ]
