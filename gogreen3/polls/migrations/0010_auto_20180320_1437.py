# Generated by Django 2.0.1 on 2018-03-20 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20180320_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='acao',
            field=models.IntegerField(blank=True, verbose_name='Acao'),
        ),
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.IntegerField(blank=True, verbose_name='Status'),
        ),
    ]
