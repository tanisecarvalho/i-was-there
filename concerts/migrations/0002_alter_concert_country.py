# Generated by Django 3.2.20 on 2023-08-26 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concerts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='country',
            field=models.CharField(max_length=200),
        ),
    ]