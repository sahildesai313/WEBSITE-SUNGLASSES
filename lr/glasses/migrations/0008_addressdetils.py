# Generated by Django 5.0 on 2024-02-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glasses', '0007_alter_femaleproduct_id_alter_maleproduct_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='addressdetils',
            fields=[
                ('name', models.CharField(max_length=20)),
                ('phone', models.IntegerField(max_length=10)),
                ('locality', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('pincode', models.IntegerField(max_length=6)),
                ('city', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]