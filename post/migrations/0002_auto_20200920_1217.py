# Generated by Django 3.1 on 2020-09-20 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
