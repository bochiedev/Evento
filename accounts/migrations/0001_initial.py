# Generated by Django 2.2.1 on 2019-05-19 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(max_length=20)),
                ('username', models.CharField(max_length=50)),
                ('secret', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
