# Generated by Django 4.0.4 on 2022-04-12 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funding',
            name='funding_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]