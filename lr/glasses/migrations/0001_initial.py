# Generated by Django 5.0 on 2024-04-03 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50)),
                ('massage', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('fullname', models.CharField(default='', max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=8)),
                ('confirmpassword', models.CharField(max_length=8)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='', max_length=1)),
                ('otp', models.CharField(blank=True, max_length=4, null=True)),
                ('country', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=250)),
                ('price', models.IntegerField()),
                ('modelnumber', models.CharField(default='', max_length=10)),
                ('framesize', models.CharField(default='', max_length=10)),
                ('framecolour', models.CharField(default='', max_length=50)),
                ('framewidth', models.CharField(default='', max_length=10)),
                ('image', models.ImageField(default=None, upload_to='image')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.IntegerField(choices=[(1, 'MALE'), (2, 'FEMALE')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locality', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('pincode', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=10)),
                ('state', models.CharField(max_length=10)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glasses.person')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameoncard', models.CharField(max_length=250)),
                ('cardno', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=10)),
                ('cvv', models.CharField(max_length=10)),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='glasses.person')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='glasses.product')),
            ],
        ),
    ]
