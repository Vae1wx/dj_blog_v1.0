# Generated by Django 3.0.6 on 2020-06-09 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0002_readdetail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReadDetail',
        ),
    ]