# Generated by Django 3.0.3 on 2020-04-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0011_geolayermodel_style_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoServerBaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='localhost', max_length=50)),
                ('port', models.IntegerField(default=8082)),
            ],
            options={
                'db_table': 'geo_serverinfo',
            },
        ),
    ]