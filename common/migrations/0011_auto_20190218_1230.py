# Generated by Django 2.1.7 on 2019-02-18 07:00

from django.db import migrations, models


class Migration(migrations.Migration):
  dependencies = [
    ('common', '0010_apisettings'),
  ]

  operations = [
    migrations.AlterField(
      model_name='apisettings',
      name='apikey',
      field=models.CharField(blank=True, max_length=16),
    ),
  ]
