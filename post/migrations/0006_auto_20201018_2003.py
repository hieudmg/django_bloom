# Generated by Django 3.1 on 2020-10-18 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20201018_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(to='post.Category'),
        ),
    ]
