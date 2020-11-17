# Generated by Django 2.2.5 on 2020-11-06 11:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20201106_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='accuracy',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='check_in',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='cleanliness',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='communication',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='location',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='value',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]